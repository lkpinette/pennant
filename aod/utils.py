import nltk

def createCorpus(fildir):
    my_sent_tokenizer = nltk.RegexpTokenizer('[^.!?]+')
    # Create the new corpus reader object.
    corpus = nltk.corpus.PlaintextCorpusReader(
    fildir, '.*\.txt', sent_tokenizer=my_sent_tokenizer)
    return corpus

def linelist(filename):
    lines = []
    for line in open(filename):
        parts = line.strip().split(':')
        lines.append(parts[0].strip())
    return lines
