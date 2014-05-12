from __future__ import division
import nltk, urllib2, re, time, random, os
from nltk.probability import *
from nltk.tag import pos_tag
from nltk.corpus import stopwords
import utils

dwords = [r'\bgross\b', r'\bdisgusting\b', r'\brevolting\b', r'\brepulsive\b', r'\bicky\b', r'\byucky\b', r'\bnasty\b', r'\bvile\b', r'\brepugnant\b', r'\brepellent\b', r'\bnauseating\b', r'\bheinous\b']
twords = ['gross', 'disgusting', 'revolting', 'repulsive', 'icky', 'yucky', 'nasty', 'vile', 'repugnant', 'repellent', 'nauseating', 'heinous']
enstop = stopwords.words('english')

# These are the nouns I used in the presentation
concrete = utils.linelist('wordlists/concrete.txt')
general =  utils.linelist('wordlists/general.txt')
abstract = utils.linelist('wordlists/abstract.txt')
            
    
def fdWordOfType(postags, doprint=False):
    ''' gets freqDist for all words of a certain tag if not in stopwords
        and is alpha
    '''
    awords = [item[0].lower() for item in bocl_tw if item[1] in postags and
        item[0].lower() not in enstop and item[0].isalpha()]
    afd = FreqDist(awords)
    an2pls = [(afd[word], word) for word in list(set(awords))]
    an2pls.sort()
    
    if doprint == True:
        for an in an2pls:
            if an[0] > 11:
                print '%s : %s' %(an[1], an[0])

bocl = utils.createCorpus('boc')
fids = bocl.fileids()
boclsents = bocl.sents()
bocl_tagged = nltk.corpus.TaggedCorpusReader('tagged', '.*\.txt')
bocl_ts = bocl_tagged.tagged_sents()
bocl_tw = bocl_tagged.tagged_words()

# To get the frequency of words tagged only as nouns, which I'm playing
# with in my latest versions but don't have stable yet, untag the following:

#fdWordOfType(['NN', 'NNS'], True)

gdict = {}
for word in twords:
    gdict[word] = {'concrete':0, 'general':0, 'abstract':0}

ndict = {'concrete':concrete, 'general':general, 'abstract':abstract}


def printProbs():
    ''' Get and print the probability of a given adjective occurring with
        each class of noun
        Currently uses global variables, will later change it to be self-
    '''
    for gkey in gdict:
        for s in bocl.sents():
            if gkey in s:
                for w in s:
                    if w in concrete:
                        gdict[gkey]['concrete'] += 1
                    elif w in general:
                        gdict[gkey]['general'] += 1
                    elif w in abstract:
                        gdict[gkey]['abstract'] += 1
    ##    print gdict[gkey]['concrete']
    ##    print gdict[gkey]['general']
    ##    print gdict[gkey]['abstract']
        gtotal = gdict[gkey]['concrete'] + gdict[gkey]['general'] + gdict[gkey]['abstract']
        print gkey + ' : ' + str(gtotal)
        for ckey in gdict[gkey]:
            print '%s : %s'%(ckey, gdict[gkey][ckey]/gtotal *100)
        print '\n'
        
printProbs()
