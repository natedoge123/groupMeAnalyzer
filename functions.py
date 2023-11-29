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
        #   del jsonFile[i]['attachments']
        #   del jsonFile[i]['avatar_url']
        #   del jsonFile[i]['group_id']
        #   del jsonFile[i]['id']
        #   del jsonFile[i]['sender_type']
        #   del jsonFile[i]['source_guid']
        #   del jsonFile[i]['system']
        #   del jsonFile[i]['pinned_at']
        #   del jsonFile[i]['pinned_by']
        #   del jsonFile[i]['platform']
        #   del jsonFile[i]['user_id']

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
        if (message['sender_id'].isnumeric()):
            sender = idList.index(message['sender_id'])
            for liker in message['favorited_by']:
                likerIndex = idList.index(liker)
                favArray[sender][likerIndex] += 1

    return favArray



def likedMessagesPercentage(likeMatrix, messageCounts):
    dim = (len(messageCounts))
    likeMatrixPercent = np.zeros((dim, dim))
    print(messageCounts)

    for i in range(len(messageCounts)):
        for j in range(len(likeMatrix)):
            likeMatrixPercent[i][j] = round((likeMatrix[i][j]/messageCounts[i])*100, 2)

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

def drawLikedMessages (nameList, favArray, saveLocation):
    nameList = column(nameList, 1)

    fig, ax = plt.subplots()
    im = ax.imshow(favArray)

    plt.xlabel('Message Liker')
    plt.ylabel('Message Sender')

    ax.set_xticks(np.arange(len(nameList)), labels = nameList)
    ax.set_yticks(np.arange(len(nameList)), labels = nameList)

    plt.setp(ax.get_xticklabels(), rotation = 45, ha = 'right', rotation_mode = 'anchor')
    for i in range(len(nameList)):
        for j in range(len(nameList)):
            text = ax.text(j, i, favArray[i,j], ha = 'center', va = 'center', color = 'w')

    ax.set_title('Who Liked Whose Message')
    fig.tight_layout()
    plt.savefig(saveLocation, format = 'png')

    return 0




##########################################################################
#   Forth part adds addition functions that are needed for general use

##########################################################################

def column(matrix, i):
    return [row[i] for row in matrix]

