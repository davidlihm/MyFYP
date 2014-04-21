resultPath = "D:\\Dropbox\\FYP\\project\\CSDMC2010_SPAM\\SPAMTrain.label"
resultPathTest = "D:\\Dropbox\\FYP\\project\\t\\label.txt"


def getCSDMCResult(path):
    ''' To parse the email set
        Return List of results
        Result:[0/1, Filename]
    '''
    f = open(path, "r")
    l = []
    for line in f:
        l.append(line[:-1].split(' '))
    return l

