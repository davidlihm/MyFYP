'''
Get text contents of emails, process them.
Count the occurrence of every word in these text contents.
Filter some high-frequency words.
Makes use of Porter Stemmer Algo., whose original source code is got
the founder's site
'''

import re
import Port_stem
from emailFileProcessor import emailParser

# Drop these words because they are meaningless.
# Actually, we can also call it stopword list
dropList = ['an', 'the', 'in', 'of', 'on', 'to',
                'as', 'for', 'it', 'that', 'this', 'those', 'these', 'by', 'is', 'are', 'was', 'were', 'be', 'being',
                'you', 'and', 'with', 'do','did','q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f',
                'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'c', 'v', 'b', 'n', 'm', '[', ']', '\\', ';', "'", ',', '.',
                '?', '"', '{', '}', '|', '/', '-', '_', '=', '+', '`', '~','\n' ]
def getEmailContents(wholeContent):
    # Co-operate with email parser. receive a parsed tuple.
    # Format of para: (subject, payload)
    if not len(wholeContent) == 2:
        return
    subject, payload = wholeContent
    body = re.sub(r'.*(?=<body)', '', payload,
                  count=1, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    list_body = getWordList(body)
    list_subject = getWordList(subject)
    return (list_subject, list_body)

def getOriEmailContents(wholeContent):
    # Co-operate with email parser. receive a parsed tuple.
    # Format of para: (subject, payload)
    if not len(wholeContent) == 2:
        return
    subject, payload = wholeContent
    body = re.sub(r'.*(?=<body)', '', payload,
                  count=1, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    list_body = getOriWordList(body)
    list_subject = getOriWordList(subject)
    return (list_subject, list_body)
def getContentsFromFile(file):
    # No use
    subject, payload = emailParser(file)
    body = re.sub(r'.*(?=<body)', '', payload,
                  count=1, flags=re.IGNORECASE | re.MULTILINE | re.DOTALL)
    list_body = getWordList(body)
    list_subject = getWordList(subject)
    return (list_subject, list_body)


def removeHTMLTags(text):
    # No use
    ''' Remove the <xxx> tags in text
        Return String. of text
        Only work for getWordList()
    '''
    return re.sub('<[^<]+>', '', text)


def removePuntuation(text):
    # No use
    ''' Remove all puntuation marks: ?.,;'...
        text: String content with marks.
        Only work for getWordList()
    '''
    return re.split('[^-\w]+', text)


def getWordList(string):
    L = Port_stem.getWordList(string, dropList)
    return L
    ''' Work with getEmailContents()
        string: html string
        Return the List of words parsed from text
    '''
    

def getOriWordList(string):
    return removePuntuation(removeHTMLTags(string))


def filterWord(word):
    passed = True

    word = word.lower()
    if len(word) < 2:
        passed = False
    if word in dropList:
        passed = False
    if word.isdigit():
        passed = False
    return passed


def testText():
    # No use
    import emailFileProcessor

    text = emailFileProcessor.test1()[1]
    return getWordList(text)
	
