import pandas as pd
import numpy as np


#these lists contain tuples (chantIndex, chantMode, chantVolPiano)
mode1 = []
mode2 = []
mode3 = []
mode4 = []
mode5 = []
mode6 = []
mode7 = []
mode8 = []
#min and max of length of note groups
MINLEN = 5

#the amount of results per mode to get
TOPNUM = 20

#=True will include repeated notes
REPEATED = True

CSV_DATA = pd.read_csv("../Data/CHNT_DATAFlats.csv");


#this function sorts all of the chants into their mode 
#and keeps only groups of notes that are between min and max len
def addToModeList():

    #takes in a string a returns a string with no 2 repeated chars beside eachother
    def removeRepeated(word):
        charList = list(word)
        for char in range(0,len(charList)):
            if (char >= len(charList)-1):
                break
            while (charList[char] == charList[char+1]):
                charList.pop(char)
                if (char >= len(charList)-1):
                    break
        returnString = ''.join(charList)
        return (returnString)


    for index, row in CSV_DATA.iterrows():

        #some 'Mode' columns have '?' and will send an error
        try:
   
            mode = int(row['Mode'].strip("'"))
            chant = row['FlatVolPiano']
            chant = chant.replace('yb','B')
            chant = chant.replace('ij','J')    
            chant = chant.split('---') 
            final = row['Final']
            newchant = []
            for i in range(0,len(chant)):
                chant[i] = chant[i].replace('-','')
                chant[i] = chant[i].replace(';','')
                chant[i] = chant[i].replace('<','')
                if (not REPEATED):
                    chant[i] = removeRepeated(chant[i])

                #OLD - we want all of the possible phrases
                #if (len(chant[i]) >= MINLEN and len(chant[i]) <= MAXLEN):
                if (len(chant[i]) >= MINLEN):
                	tempString = chant[i]
                	while (len(tempString) >= MINLEN):
                         substring = tempString[:MINLEN]
                         tempString = tempString[1:]                  
                         newchant.append(substring)

            #now have the index, mode, and chant phrases between min and max length
            #add it to the correct mode
            if (mode == 1):
                mode1.append((index, mode, newchant))
            if (mode == 2):
                 mode2.append((index, mode, newchant))
            if (mode == 3):
                mode3.append((index, mode, newchant))
            if (mode == 4):
                mode4.append((index, mode, newchant))                                 
            if (mode == 5):
                mode5.append((index, mode, newchant))
            if (mode == 6):
                mode6.append((index, mode, newchant))
            if (mode == 7):
                mode7.append((index, mode, newchant))
            if (mode == 8):
                mode8.append((index, mode, newchant))

        except Exception as e: print(e)

#compares a list of n tuples and returns a list of most commen strings
#return list of tuples ([chantIndexs], howManyTimes, chantVolPiano)
def compList(mode_list, n):

    #keeps a list of max n things
    #PARAMS: max-n from function, finalList-a sorted list (based on count) to be inputed into
    #        indexList-the chants where it appears
    def appendMax(max, finalList, indexList, count, chant):
        def countFind(elem):
            return elem[1]
        #check if current chant phrase is already is list
        for entry in finalList:
            if (entry[2] == chant):
                return finalList
        #put in list of there is space
        if (len(finalList) < max):
            finalList.append((indexList, count, current))
        else:
            if (count > finalList[max-1][1]):
                finalList.pop(max-1)
                finalList.append((indexList, count, current))
                finalList.sort(key=countFind, reverse=True)
        return finalList

    current = ''
    countList = []
    for i in range(0,len(mode_list)):
        temp = mode_list[i][2]
        index = mode_list[i][0]
        for j in range(0, len(temp)):
            count = 0
            current = temp[j]
            indexList = [index]
            for a in range(0,len(mode_list)):
                if (mode_list[a][2].count(current) > 0 and mode_list[a][0] != index):
                    indexList.append(mode_list[a][0])
            
            count = len(indexList)
            countList = appendMax(n, countList, indexList, count, current)

    return countList


#print list of tuples ([chantIndexs], howManyTimes, chantVolPiano) that looks good
def mostCommonPrint(x_mostCommon):
    for i in range(0, len(x_mostCommon)):
        #print(str(i+1) + ". Found in chants indices: ", end='')
        #print((x_mostCommon[i][0]), end='')
        print("Found " + str(x_mostCommon[i][1]) + ' TIMES')
        print("Chant: " + x_mostCommon[i][2] + "\n")


##### MAIN #####

addToModeList()
print(len(mode1))
mostCommon1 = compList(mode1, TOPNUM)
print(len(mode2))
mostCommon2 = compList(mode2, TOPNUM)
print(len(mode3))
mostCommon3 = compList(mode3, TOPNUM)
print(len(mode4))
mostCommon4 = compList(mode4, TOPNUM)
print(len(mode5))
mostCommon5 = compList(mode5, TOPNUM)
print(len(mode6))
mostCommon6 = compList(mode6, TOPNUM)
print(len(mode7))
mostCommon7 = compList(mode7, TOPNUM)
print(len(mode8))
mostCommon8 = compList(mode8, TOPNUM)



print("--------- MODE D ---------")
print("MODE 1")
mostCommonPrint(mostCommon1)

print("MODE 2")
mostCommonPrint(mostCommon2)

print("\n\n--------- MODE E ---------")
print("MODE 3")
mostCommonPrint(mostCommon3)
print("MODE 4")
mostCommonPrint(mostCommon4)

print("\n\n--------- MODE F ---------")
print("MODE 5")
mostCommonPrint(mostCommon5)
print("MODE 6")
mostCommonPrint(mostCommon6)

print("\n\n--------- MODE G ---------")
print("MODE 7")
mostCommonPrint(mostCommon7)
print("MODE 8")
mostCommonPrint(mostCommon8)













