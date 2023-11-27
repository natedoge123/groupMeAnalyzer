import json
import datetime
import os
import numpy as np
import time

import functions as fnc

########################
#   Load Section
########################

fileReadLocation = input("What is the path to the directory? \n")
fileReadLocation = "/home/nate/Documents/dataFiles/gmArchive/20231104/"
fileWriteLocation = fileReadLocation

readNames = fileReadLocation + "conversation.json"
readMessages = fileReadLocation + "message.json"

startTime = time.time()

names = fnc.nameList(fnc.jsonLoader(readNames))
messages = fnc.jsonCleaner(fnc.jsonLoader(readMessages))

messsages = fnc.nameUpdate(messages, names)
fnc.jsonWriter(messages, fileWriteLocation, 'newMessage')
print(messages[2])
print(names)

########################
#   Analysis Section
########################

messageCount = fnc.messageCountPerPerson(messages, names)

likedMessage = fnc.likedMessages(messages, names)


########################
#   Graph Section
########################

#   Plot Total Messages
fnc.drawMessageCount(names, messageCount, (fileWriteLocation + 'messageCount.png'))

#   Plot Like Numbers

#   Plot Like Percentages


print("Complete")
print("Run Time %s seconds" % (time.time() - startTime))
