from __future__ import division
import nltk, urllib2, re, time, random, os
from nltk.probability import *
from nltk.tag import pos_tag
from nltk.corpus import stopwords
import utils

dwords = [r'\bgross\b', r'\bdisgusting\b', r'\brevolting\b', r'\brepulsive\b', r'\bicky\b', r'\byucky\b', r'\bnasty\b', r'\bvile\b', r'\brepugnant\b', r'\brepellent\b', r'\bnauseating\b', r'\bheinous\b']
twords = ['gross', 'disgusting', 'revolting', 'repulsive', 'icky', 'yucky', 'nasty', 'vile', 'repugnant', 'repellent', 'nauseating', 'heinous']

# These are the nouns I used in the presentation
concrete = utils.linelist('wordlists/concrete.txt')
general =  utils.linelist('wordlists/general.txt')
abstract = utils.linelist('wordlists/abstract.txt')
            

bocl = utils.createCorpus('boc')
fids = bocl.fileids()
boclsents = bocl.sents()
bocl_tagged = nltk.corpus.TaggedCorpusReader('tagged', '.*\.txt')
bocl_ts = bocl_tagged.tagged_sents()
bocl_tw = bocl_tagged.tagged_words()

gdict = {}
for word in twords:
    gdict[word] = {'concrete':0, 'general':0, 'abstract':0}

ndict = {'concrete':concrete, 'general':general, 'abstract':abstract}

def printProbs():
    ''' Get and print the probability of a given adjective occurring with
        each class of noun
        Currently uses global variables, will later change it to be self-
    '''
    ants = []
    for ts in bocl_tagged.tagged_sents():
        s = [tw[0] for tw in ts]
        for gkey in gdict:
            if gkey in s:
                for w in s:
                    for nt in ndict:
                        if w in nt:
                            ants.append((gkey, nt))

    antcfd = ConditionalFreqDist(ants)
    antcfd.tabulate()
    antcpd = ConditionalProbDist(antcfd, MLEProbDist)
    for gkey in gdict:
        print gkey, ':'
        for nt in ndict:
            print '%s : %s'%(nt, antcpd[gkey].prob(nt) *100)
        print '\n'
        
printProbs()
