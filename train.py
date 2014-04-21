from textProcessor import *
import database
from emailFileProcessor import *
from result import *
# Make use of database 1.


#train_path = 'D:\\Dropbox\\FYP\\project\\CSDMC2010_SPAM\\TRAINING'
train_ham1 = 'D:\\David\\SomeData\\data\\easy_ham_2'
train_ham2 = 'D:\\David\\SomeData\\data\\easy_ham'
train_spam1 = 'D:\\David\\SomeData\\data\\spam_2'
train_spam2 = 'D:\\David\\SomeData\\data\\spam'

#train_spam3 = 'D:\\David\\SomeData\\spam\\spam4'

def train_with_path(train_path, isHam):
    conn = database.getDBConnect()
    elist = getEmailFiles(train_path)
    print('Get Result Label of '+train_path)
    #resultList = getCSDMCResult(resultPath)
    #print('dataset Result got.')
    count = 0
    for e in range(len(elist)):
        whole = emailParser(elist[e]) #list of (subject,payload)
        contents = getEmailContents(whole) # word list, without useless contents,[subject, body]
        #result = resultList[e][0] #list of 0s and 1s.
        #print(len(contents[0])) #list of words from subject
        #print(len(contents[1])) #list of words from payload
        for i in range(len(contents[0])):
            database.processWords(conn, contents[0][i], True, isHam)
        for j in range(len(contents[1])):
            database.processWords(conn, contents[1][j],  False, isHam)
        #processContent(contents)
        count = count + 1
        #print(count)
        if count % 50 == 0:
            print(count)
            conn.commit()

    print("++++++++++++++FINISH+++++++++++++")
    print("Total files")
    print(count)
    conn.close()

if __name__ == "__main__":

    train_with_path(train_ham1, True)
    #train_with_path(train_spam, False)
    #train_with_path(train_spam, False) #TRAINED
    train_with_path(train_ham2, True)  #TRAINED
    train_with_path(train_spam2, False)
    train_with_path(train_spam1, False)
