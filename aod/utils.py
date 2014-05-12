import nltk

dwords = [r'\bgross\b', r'\bdisgusting\b', r'\brevolting\b', r'\brepulsive\b', r'\bicky\b', r'\byucky\b', r'\bnasty\b', r'\bvile\b', r'\brepugnant\b', r'\brepellent\b', r'\bnauseating\b', r'\bheinous\b']
twords = ['gross', 'disgusting', 'revolting', 'repulsive', 'icky', 'yucky', 'nasty', 'vile', 'repugnant', 'repellent', 'nauseating', 'heinous']

def createCorpus(fildir):
    my_sent_tokenizer = nltk.RegexpTokenizer('[^.!?]+')
    # Create the new corpus reader object.
    corpus = nltk.corpus.PlaintextCorpusReader(
    fildir, '.*\.txt', sent_tokenizer=my_sent_tokenizer)
    return corpus

def linelist(filename, rcnt = False):
    lines = []
    counts = []
    for line in open(filename):
        parts = line.strip().split(':')
        lines.append(parts[0].strip())
        counts.append(parts[1].strip())
    if rcnt == True:
        return lines, counts
    return lines

