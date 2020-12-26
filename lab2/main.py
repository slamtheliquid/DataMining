import csv
import math
import re

from nltk import PorterStemmer
from nltk.corpus import stopwords

porter = PorterStemmer()


def isStopWord(word):
    if word in stopwords.words('english'):
        return True
    return False


def convertStringToListAndStem(string):
    li = list(string.split(" "))
    res = []
    for l in li:
        l = l.lower()
        l = porter.stem(l)
        if not isStopWord(l) and len(l) > 0:
            res = res + [l]
    return res

def countUnique():
    uniqueList=[]
    with open('../lab1/hum.csv', newline='') as csvfile:
        humreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for h in humreader:
            if h not in uniqueList:
                uniqueList.append(h)
    with open('../lab1/spam.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for h in spamreader:
            if h not in uniqueList:
                uniqueList.append(h)
    return len(uniqueList)




def deleteSpecialSymbolsFromString(string):
    string = re.sub('[^a-zA-Z \n]', ' ', string)
    return convertStringToListAndStem(string)


def lab2Main():
    humCount = 0
    spamCount = 0
    with open('../lab1/hum.csv', newline='') as csvfile:
        humreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for h in humreader:
            humCount = humCount + int(h[1])
    with open('../lab1/spam.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for h in spamreader:
            spamCount = spamCount + int(h[1])
    messageHumDict = {}
    messageSpamDict = {}
    spamJustMulti=1
    humJustMulti=1;
    spam = 0
    hum = 0
    z = 1;  # коеф размытия

    humDictFromFile = {}
    spamDictFromFile = {}
    uniq=countUnique()
    with open('../lab1/hum.csv', newline='') as csvfile:
        humreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for f in humreader:
            humDictFromFile[f[0]] = f[1]
    with open('../lab1/spam.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for f in spamreader:
            spamDictFromFile[f[0]] = f[1]
    while (True):
        messageHumDict = {}
        messageSpamDict = {}
        spamJustMulti = 1;
        humJustMulti = 1;
        spam = 0
        hum = 0
        print("Enter message")
        strn = str(input())
        messageList = deleteSpecialSymbolsFromString(strn)
        for key in messageList:
            if key in humDictFromFile.keys():
                humJustMulti *= (int(humDictFromFile.get(key)) + z) / (humCount + z * uniq)
                messageHumDict.update({key: math.log((int(humDictFromFile.get(key)) + z) / (humCount + z * uniq))})
            else:
                humJustMulti *=z / (humCount + z * uniq)
                messageHumDict.update({key: math.log(z / (humCount + z * uniq))})
        for key in messageList:
            if key in spamDictFromFile.keys():
                spamJustMulti *= (int(spamDictFromFile.get(key)) + z) / (spamCount + z * uniq)
                messageSpamDict.update({key: math.log((int(spamDictFromFile.get(key)) + z) / (spamCount + z * uniq))})
            else:
                spamJustMulti *= z / (spamCount + z * uniq)
                messageSpamDict.update({key: math.log(z / (spamCount + z * uniq))})
        hum=hum+math.log(humCount/(humCount+spamCount))
        spam = spam + math.log(spamCount / (humCount + spamCount))
        humJustMulti*=humCount/(humCount+spamCount)
        spamJustMulti*=spamCount/(humCount+spamCount)
        print("Hum multi=",humJustMulti)
        print("spam multi=",spamJustMulti)
        for h in messageHumDict.values():
            hum = hum + h
        for h in messageSpamDict.values():
            spam = spam + h

        if (hum / (hum + spam) < 0.50):  
            print("It's hum, good")
        else:
            print("It's spam.")



lab2Main()
