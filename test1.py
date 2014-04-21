__author__ = 'User'
import database
from emailFileProcessor import getEmailFiles, emailParser
from textProcessor import getEmailContents
import threading


t = threading.Thread
mylock = threading.RLock()
spam_path1 = "D:\\David\\SomeData\\data\\test_spam"
ham_path1 = "D:\\David\\SomeData\\data\\test_ham"
spam_path2 = "D:\\David\\SomeData\\s"
ham_path2 = "D:\\David\\SomeData\\h"
spam_files = getEmailFiles(spam_path2)
ham_files = getEmailFiles(ham_path2)
#print(spam_files[:10])
#count_all = [0,0,0,0]
#count_correct = [0,0,0,0]


def compute(word_list, factor=0.9, threshold=0.5):
    '''Pass in a list of words
        Calculate the prob. of being spam
        isHam : The tested dataset is a Ham set
    '''
    overall_spam,overall_ham = 1, 1
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
            spam_prob = float(spam)/(spam+ham)
            ham_prob = 1 - spam_prob
            overall_spam = overall_spam * spam_prob + overall_spam
            overall_ham = overall_ham * ham_prob + overall_ham
    P = factor*overall_spam / (factor*overall_spam+(1-factor)*overall_ham)

    if(P>threshold):
        return False
        #print('spam')
        #print(str(count_all[index])+' , '+ str(count_correct[index]))
    else:
        return True
        #print('ham')


def run(start, end, index=0, isHam=False):
    #global count_all
    #global count_correct
    if isHam is True:
        files = ham_files
    else:
        files = spam_files
    for f in range(start,end):
        #result_file = open('./result.txt', 'a')
        print('file opened')
        factor = float(f/20)
        for ff in range(1,4):
            count_all = 0
            count_correct = 0
            thres = float(ff/4)
            print('factor is : %f \t Threshold is %f' % (factor,thres))
            for e in files:
                (subject, payload) = emailParser(e)
                contents = getEmailContents((subject, payload))
                whole = contents[0]
                whole.extend(contents[1])
                whole = list(set(whole))
                #print(e)
                count_all= count_all + 1
                r = compute(whole, factor=factor, threshold=thres)
                if r and isHam: #isHam=True , r=True
                    count_correct = count_correct + 1
                if (not r) and (not isHam): #isHam=False, r=False
                    count_correct = count_correct + 1

                print('%d,%d at thread %d' % (count_correct,count_all, index))
            rate = float((count_correct / count_all))
            print('Final: %d,%d at thread %d' % (count_correct,count_all, index))
            print('rate is : %f' % rate)
            result = 'Factor: %.4f \t Threshold: %.4f \t Probability: %.4f \t with  (%d,%d)\n' % (factor, thres, rate, count_correct, count_all)
            #result = result+'factor: '+str(factor)+'\t probability: '+str(rate)+'\n'
            print(result)
            print('At thread '+ str(index))
            mylock.acquire()
            result_file = open('./result3_spam.txt', 'a')
            result_file.write(result)
            result_file.close()
            mylock.release()


t0 = t(target=run,args=(1,6,0,False))
t1 = t(target=run,args=(6,11,1,False))
t2 = t(target=run,args=(11,16,2,False))
t3 = t(target=run,args=(16,21,3,False))
t0.start()
t1.start()
t2.start()
t3.start()
