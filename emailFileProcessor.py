import os
import email.parser


def getEmailFiles(path):
    ''' Get the path of folder containing all .eml files
        return: List. the whole path of eml file, list of String'''
    import glob # Pathname Pattern matching lib

    if os.path.isdir(path):
        #return glob.glob(path + '\\*.eml')
        return glob.glob(path + '\\*')
    else:
        print("You need to enter a path of folder")# If the arg is not a path, error
        return


def emailParser(emlFileName):
    ''' Parse a email file.
        Get the path of one .eml file
        return: Tuple. T[0]:subject; T[1]:content
    '''
    if not os.path.exists(emlFileName):
        print("File not found: " + str(emlFileName))
        return
    file = open(emlFileName, "r", encoding='L1') # charset:L1, Latin-1

    msg = email.message_from_file(file)
    file.close()
    subject = str(msg.get('subject'))
    p = msg.get_payload()
    if type(p) == type(list()):
        payload = str(p[0])
    else:
        payload = str(p)

    return (subject.lower(), payload.lower())


def parseAll(path, func):
    ''' Receive a folder path and get a list of contents. Then, process these contents.
    path: folder that contains .eml files.
    func: a function to do on EACH email contents.
    Process every content(sub,pay) with the function func.'''
    files = getEmailFiles(path)
    for f in files:
        content = emailParser(f)
        func(content)


def test(path='D:\\Study\\FYP\\project'):
    files = getEmailFiles(path)
    for i in range(len(files)):
        file = emailParser(files[i])


def test1(path='D:\\Study\\FYP\\project'):
    ''' Test one file
        return Tuple(subject, content)
    '''
    files = getEmailFiles(path)
    return emailParser(files[0])






	



