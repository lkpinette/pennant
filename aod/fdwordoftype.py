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
        
writeWL(wlist, 'wordlists/rawwl.txt')
