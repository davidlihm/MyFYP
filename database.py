import sqlite3

database_path = 'D:\\Dropbox\\FYP\\project\\database.db'
# c.execute(''' create table if not exists words (
# 					name text,
# 					freq_spam integer,
# 					freq_not integer
# 					)''')
def getDBConnect(path = database_path):
    conn = sqlite3.connect(path)
    return conn


def processWords(conn, wordName, isSubject, isHam, num=1):
    ''' isSubject:Bool; True:subject; False:content
        isHam:Bool; True:Ham; False:Spam
        '''
    cursor = conn.cursor()
    #if type(isSubject)!=bool or type(isSpam)!=bool
    #	print('The property isSubject or isHam must be bool')
    #	return
    wordList = cursor.execute('select name from words').fetchall()
    wordList = [x[0] for x in wordList]
    #isSubject = int(isSubject)
    isSpam = int(isHam)
    boolType = (isSubject << 1) + isSpam #11:T,T:3; 10:T,F:2; 01:F,T:1; 00:F,F:0;
    if wordName in wordList:
        #print('start UPDATE')
        updateWord(cursor, wordName, boolType, num)
    #print('END update')
    else:
        #print('start INSERT')
        insertWord(cursor, wordName, boolType, num)
    #print('END Insert')
    #conn.commit()


def updateWord(cursor, wordName, boolType, num):
    #cursor = conn.cursor()
    wordType = {
    0: 'content_spam',
    1: 'content_ham',
    2: 'subject_spam',
    3: 'subject_ham'
    }[boolType]
    para = (wordName, num, wordName)
    q = 'update words set %s = ( select %s from words where name = ' % (wordType, wordType)
    cursor.execute(q + ''' ?)+ ? where name = ?''', para)

#c.execute('''update words set content_spam =
# 	(select content_spam from words where name = 'dd')+10
# 	where name='dd' ''')


def insertWord(cursor, wordName, boolType, num):
    #cursor = conn.cursor()
    '''
        0: FF: Content + Spam : 0001
        1: FT: Content + Ham : 0010
        2: TF: Subject + Spam : 0100
        3: TT: Subject + Ham : 1000
    '''
    para = {
    0: (wordName, 0, 0, 1, 0, num, 1),
    1: (wordName, 0, 0, 1, num, 0, 1),
    2: (wordName, 0, num, 1, 0, 0, 1),
    3: (wordName, num, 0, 1, 0, 0, 1)
    }[boolType]
    cursor.execute('''insert into words values (?,?,?,?,?,?,?)''', para)


def retrievalWord(conn, word):
    cursor = conn.cursor()
    sql_count = '''SELECT subject_spam+content_spam AS spam,
                    subject_ham+content_ham AS ham FROM Words
                    WHERE name = ?'''
    row = cursor.execute(sql_count, (word,))
    n = row.fetchone()
    if n is None:
        return 0
    else:
        return n #(spam,ham)0: no exist;  >0: num of hits

# def insertWord(word, isSpam, num=1):
# 	wordList = c.execute('select name from words').fetchall()
# 	wordList = [x[0] for x in wordList]
# 	if word in wordList:
# 		if isSpam:
# 			c.execute('''update words set freq_spam = (
# 				select freq_spam from words where name = ?)+?
# 				where name = ?''', (word, num, word))
# 		else:
# 			c.execute('''update words set freq_not = (
# 				select freq_not from words where name = ?)+?
# 				where name = ?''', (word, num, word))
# 		print(c.execute('select * from words where name = ?', (word,) ).fetchone())
# 	else:
# 		if isSpam:
# 			c.execute('insert into words values (?,?,?)',(word,1,0))
# 			print("New Spam word: "+word)
# 		else:
# 			c.execute('insert into words values (?,?,?)',(word,0,1))
# 			print("New Not word: "+word)
# 	conn.commit()


def closeDB(conn):
    conn.commit()
    conn.close()



