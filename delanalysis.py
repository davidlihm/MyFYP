__author__ = 'User'
import database
from emailFileProcessor import getEmailFiles, emailParser
from textProcessor import getEmailContents
path='D:\\Dropbox\\FYP\project\\CSDMC2010_SPAM\\TEST\\SPAM\\18'
#spam_file = getEmailFiles(path)
probs = []
def compute(word_list, isHam = False):
    '''Pass in a list of words
        Calculate the prob. of being spam
        isHam : The tested dataset is a Ham set
    '''
    #global count_all
    #global count_correct
    overall_spam,overall_ham = 1.0, 1.0
    conn = database.getDBConnect()
    for w in word_list:
        num = database.retrievalWord(conn, w)
        if num == 0: #num=0, No this word in DB
            pass
        else:
            spam,ham = num[0],num[1]
            if spam ==0:
                spam = 1
            if ham == 0:
                ham = 1
            print("spam: %d, ham: %d" % (spam,ham))
            sum = spam+ham
            spam_prob = float(spam)/sum
            print('spam_prob: %f' % spam_prob)
            probs.append(spam_prob)
            ham_prob = 1 - spam_prob
            print('ham prob: %f' % ham_prob)
            overall_spam = overall_spam * spam_prob + overall_spam
            overall_ham = overall_ham * ham_prob + overall_ham
            print('overall_spam: %f , overall_ham: %f' % (overall_spam,overall_ham))
    P = 0.5*overall_spam / (0.5*overall_spam+0.5*overall_ham)
    print("The prob of being spam is %f" % P)
    #count_all = count_all +1
    #if(P>0.5):
    #    print('spam')
    #    if not isHam:
    #        count_correct = count_correct +1
    #else:
    #    print('ham')
    #    if isHam:
    #        count_correct = count_correct +1


(subject, payload) = emailParser(path)
contents = getEmailContents((subject, payload))
whole = contents[0]
whole.extend(contents[1])
whole = list(set(whole))
compute(whole)