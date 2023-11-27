import json
import os
import datetime
import numpy as np
import matplotlib.pyplot as plt

##########################################################################
#   The First Part is to clean up the given archive files
#   Need to get the real names and the nick names and account numbers    
##########################################################################
def jsonLoader(fileName):
    with open(fileName, encoding = "utf-8") as f:
        data = json.load(f)
    return data


def jsonWriter(file, filePath, fileName):
    saveLocation = filePath + fileName + ".json"
    with open(saveLocation, 'w') as g:
        json.dump(file, g, indent=4)


def nameList(jsonFile):
    nameList = []
    for i in range(int(len(jsonFile['members']))):
        col = []
        col.append(jsonFile['members'][i]['user_id'])
        col.append(jsonFile['members'][i]['name'])
        col.append(jsonFile['members'][i]['nickname'])
        nameList.append(col)
    return nameList

def jsonCleaner(jsonFile):
    for i in range(len(jsonFile)):
        del jsonFile[i]['attachments']
        del jsonFile[i]['avatar_url']
        del jsonFile[i]['group_id']
        del jsonFile[i]['id']
        del jsonFile[i]['sender_type']
        del jsonFile[i]['source_guid']
        del jsonFile[i]['system']
        del jsonFile[i]['pinned_at']
        del jsonFile[i]['pinned_by']
        del jsonFile[i]['platform']
        del jsonFile[i]['user_id']

        jsonFile[i]['created_at'] = datetime.datetime.fromtimestamp(jsonFile[i]['created_at']).strftime('%Y-%m-%d %H:%M:%S')

    return jsonFile

def nameUpdate(jsonFile, nameList):
    for names in nameList:
        for each in jsonFile:
            if (names[0] == each['sender_id']):
                each['name'] = names[1]
                each['nickname'] = names[2]

    return jsonFile


##########################################################################
#   Second part does the analysis and get the stats from the messages
#   Need to use the cleaned message list and the name list to do this
##########################################################################

def messageCountPerPerson(jsonFile, nameList):
    countList = []
    for names in nameList:
        count = 0
        for message in jsonFile:
            if (names[0] == message['sender_id']):
                count += 1
        countList.append(count)
    return countList

def likedMessages(jsonFile, nameList):
    idList = column(nameList, 0) 
    favArrayDim = (len(nameList))
    favArray = np.zeros((favArrayDim, favArrayDim), dtype='int')

    for message in jsonFile:
        print(message)
        sender = idList.index(message['sender_id'])


    return favArray



def likedMessagesPercentage(likeMatrix, messageCounts):

    return likeMatrixPercent


##########################################################################
#   Third part creates nice to read graphs that make the data readible
#   No one wants to read a power point slide
##########################################################################

def drawMessageCount(nameList, count, saveLocation):
    nameList = column(nameList, 1)
    barGraph = plt.barh(nameList, count)

    plt.savefig(saveLocation, format = 'png')
    

    
    return 0

def drawLikedMessages ():

    return 0




##########################################################################
#   Forth part adds addition functions that are needed for general use

##########################################################################

def column(matrix, i):
    return [row[i] for row in matrix]

