from __future__ import division
import nltk, urllib2, re, time, random, os
from nltk.probability import *
from nltk.tag import pos_tag
from nltk.corpus import stopwords
import utils

def checkLink(link, k):
    ''' checkLink is called by getBestOfLinks for each link
        It checks if the link is in the corpus file, and if it isn't
        checks if it has a word we're looking for, strips out most of the html
        tags, and creates a text file.
    '''
    pt = None
    # define filename as '[location]-[postingnumber].txt'
    filename = link[37:40] + '-' + link[41:-5] + '.txt' 
    try:
        open('data/' + filename, 'r')
    except:
        time.sleep(random.random()*2)
        page = urllib2.urlopen(link)
        text = page.read()
        getb = re.findall(r'<section id="postingbody">.+?</section>', text, re.S)
        getul = re.findall(r'<section id="postingbody">.+<ul>', getb[0], re.S)
        getcm = re.findall(r'<section id="postingbody">.+<!-- START ', getb[0], re.S)
        if len(getul)>0:
            getb = getul
            pt = 'ul'
        elif len(getcm)>0:
            getb = getcm
            #pt = 'ul'
        try:
            body = getb[0]
        except:
            print text
            print getb
        for word in dwords:
            tword = re.search(word, body)
            if tword:
                
                # crop out tags that we used to find the body
                if pt == 'ul':
                     body = body[29:-4]
                else:
                    body = body[29:-11]
                # replace newlines with nothing and <br> tags with newlines.
                # in effect, we're merely reversing what CL does
                # CL doesn't allow HTML tags in unpaid postings, which makes this
                # quite easy.  No need for beautiful soup
                body = body.replace('\n', '')
                body = body.replace('</p>', '')
                body = body.replace('<br>', '\n')
                body = body.replace('<p>', '\n')
    ##            body = body.replace('''<ul><li>it's NOT ok to contact this poster with services or other commercial interests</li></ul>''', '')
    ##            body = body.replace('''<li>t's NOT ok to contact this poster with services or other commercial interests</li>''', '')
    ##            body = body.replace('''<li>do NOT contact me with unsolicited services or offers</li>''', '')
    ##            body = body.replace('''<li>it's NOT ok to contact this poster with services or other commercial interests''', '')

                # create and write to file
                clfile = open('data/' + filename, 'w')
                clfile.write(body)
                clfile.close()
                
                print '\n\n%s\n'%word
                print body
                k = k + 1
                print k
    return k

def getBestOfLinks(spg=0,epg=47):
    ''' Look at each page of the "Best of Craigslist" and extract the links,
        then call checkLink of the link to each article.

        I had the number of pages of "best of" hard-coded, but changed it to
        the variable epg, and the start (0) to the variable npg.  This makes it
        possible to to look at any set of these pages one would wish.
        
    '''
    k = 0
    for i in range(spg,epg+1):
        bestofurl = 'http://www.craigslist.org/about/best/all/index%s00.html'%i
        bestofraw = urllib2.urlopen(bestofurl)
        bestoftxt = bestofraw.read()
        linxtxt = bestoftxt[1980:-990]
        linxeys = re.findall(r'best/[a-z]+/[0-9]+\.html', linxtxt)
        for key in linxeys:
            k = checkLink('http://www.craigslist.org/about/' + key, k)

#getBestOfLinks(0,47)


def cleanCorpus(old, new):
    ''' Strip tags from files in a corpus and put the result in a new directory
    '''

    oldcorpus = utils.createCorpus(old)
    oldids = oldcorpus.fileids()

    for oldid in oldids:
        oldtext = oldcorpus.raw(oldid)
        oldplain = re.sub('<.+?>', '', oldtext, 0, re.S)
        newfile = open(new + '/' + oldlid, 'w')
        newfile.write(oldplain)
        newfile.close()
        
#cleanCorpus('data', 'boc')

def tagCorpus(old, new):
    ''' Tags words for each file in a corpus and writes to a new directory
        Tagging this much data takes a long time, so I did that to make
        future access and code tweaks quicker.
    '''
    oldcorpus = utils.createCorpus(old)
    oldids = oldcorpus.fileids()

    for oldid in oldids:
        newfile = open(new + '/' + oldid, 'w')
        sents = oldcorpus.sents(oldid)
        for sent in sents:
            sentstr = ''
            tsent = pos_tag(sent)
            for tpl in tsent:
                sentstr = sentstr + tpl[0] + '/' + tpl[1] + ' '
            newfile.write(sentstr + '\n')
        newfile.close()

#tagCorpus('boc', 'tagged')
