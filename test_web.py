__author__ = 'User'
import database
from emailFileProcessor import getEmailFiles, emailParser
from textProcessor import getOriEmailContents
import threading
import Port_stem




def compute(word_list, factor=0.6):
    '''Pass in a list of words
        Calculate the prob. of being spam
        isHam : The tested dataset is a Ham set
    '''
    risk_set = set()
    overall_spam,overall_ham = 1, 1
    conn = database.getDBConnect()
    for w in word_list:
        ww = Port_stem.stemWord(w)
        num = database.retrievalWord(conn, ww)
        if num == 0: #num=0, No this word in DB
            pass
        else:
            spam,ham = num[0],num[1]
            if spam ==0:
                spam = 1
            if ham == 0:
                ham = 1
            spam_prob = float(spam)/(spam+ham)
            ham_prob = 1 - spam_prob
            if spam_prob > 0.5:
                risk_set.add(w)
            overall_spam = overall_spam * spam_prob + overall_spam
            overall_ham = overall_ham * ham_prob + overall_ham
    P = factor*overall_spam / (factor*overall_spam+(1-factor)*overall_ham)

    if(P>0.5):
        isHam =  False
        #print('spam')
        #print(str(count_all[index])+' , '+ str(count_correct[index]))
    else:
        isHam =  True
        #print('ham')
    return (P,isHam, risk_set)

def doPost(subject, payload):
    #(subject, payload) = emailParser(e)
    contents = getOriEmailContents((subject, payload))
    whole = contents[0]
    whole.extend(contents[1])
    whole = list(set(whole))
    #print(e)
    return compute(whole)


