import nltk, utils
enstop = nltk.corpus.stopwords.words('english')

def fdWordOfType(postags, doprint=False):
    ''' gets freqDist for all words of a certain tag if not in stopwords
        and is alpha
    '''
    awords = [item[0].lower() for item in bocl_tw if item[1] in postags and
        item[0].lower() not in enstop and item[0].isalpha()]
    afd = nltk.probability.FreqDist(awords)
    an2pls = [(afd[word], word) for word in list(set(awords))]
    an2pls.sort()
    
    if doprint == True:
        for an in an2pls:
            if an[0] > 11:
                print '%s : %s' %(an[1], an[0])

    return an2pls

bocl_tagged = nltk.corpus.TaggedCorpusReader('tagged', '.*\.txt')
bocl_tw = bocl_tagged.tagged_words()

wlist = fdWordOfType(['NN', 'NNS'])

def writeWL(wl, dest):
    rawwl = open(dest, 'w')
    for w in wl:
        if w[0]>11:
            rawwl.write(w[1] + ' : ' + str(w[0]) + '\n')
        
writeWL(wlist, 'wordlists/rawwl1.txt')

def areInSameSent(l1, l2, corpus, tags=None):
    newlist = []

    # if tags exist, search only sets of words which include those tags
    if tags != None:
        t1 = tags[0]
        t2 = tags[1]
        tt = t1 + t2
        tsents = corpus.tagged_sents()
        for ts in tsents:
            s = [tw[0] for tw in ts if tw[1] in tt]
            for w2 in l2:
                if w2 in s:
                    for w1 in l1:
                        if w1 in s:
                            newlist.append(w2)
                            #l2.remove(w2)
                            break
    # use whole sentences
    else:
        sents = corpus.sents()
        for s in sents:
            for w2 in l2:
                if w2 in s:
                    for w1 in l1:
                        if w1 in s:
                            newlist.append(w2)
                            #l2.remove(w2)
    return newlist
                    

def newNCFile(l1, oldfile, newfile, ddir = 'wordlists/'):
    oldnlist, clist = utils.linelist(ddir + oldfile, True)
    corpus = nltk.corpus.TaggedCorpusReader('tagged', '.*\.txt')
    newlist = areInSameSent(l1, oldnlist, corpus, (['JJ'], ['NN', 'NNS']))
    newfile = open(ddir + newfile, 'w')
    for i in range(0, len(oldnlist)):
        if oldnlist[i] in newlist:
            newfile.write(oldnlist[i] + ' : ' + clist[i] + '\n')
    newfile.close()

newNCFile(utils.twords, 'rawwl1.txt', 'rawwl3.txt')
