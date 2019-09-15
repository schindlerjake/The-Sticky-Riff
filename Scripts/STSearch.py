import pandas as pd
import numpy as np
import re
import collections
import math
import random


#holds data about each instance of the before and after riffs
#including (chantID,Mode,ChantString)
beforeList = []
afterList = []
#file to write the data to in a usable text data structure:
'''DATA STRUCTURE 
[ST, count,
[
['beforeriff1','count','percentage',[App],[Mode]],
['beforeriff2','count','percentage',[App],[Mode]], 
etc[],[]
],
'MID',
['afterriff1','count','percentage',[App],[Mode]],
['afterriff2','count','percentage',[App],[Mode]],
etc[],[]
]
'''
f = ''

#does the search look across words?
crossingwords = False

#max length of the before and after riffs
riffLength = 3

numberOfResults =6

#chant list default (chantID,Mode,ChantString)
chantList = []
#file
CSV_DATA = pd.read_csv("../Data/CHNT_DATAFlats.csv");


def AddToChantList():
    for index, row in CSV_DATA.iterrows():
    #some 'Mode' columns have '?' and will send an error
    #Put into a list of (chantID,Mode,ChantString)
        try:
        	if (True):
	            mode = int(row['Mode'].strip("'"))
	            chant = row['FlatVolPiano']
	            chant = chant.replace('---','.')
	            chant = chant.replace('yb','B')
	            chant = chant.replace('ij','J')            
	            for i in range(0,len(chant)):
	                chant = chant.replace('-','')
	            chantList.append((index, mode, chant))
        except Exception as e: print('')



def CheckBeforeAndAfter(i, middleRiff):
	curChant = i[2]
	#tracks where the middle riff is found in the current chant
	#WOW that regular expression is great!
	foundRiffIndices = [m.start() for m in re.finditer('(?='+middleRiff+')', curChant)]
	#go through each index and find the before and after riffs
	before = ''
	after = ''

	#go through each found index spot
	for ind in foundRiffIndices:
		before = ''
		after = ''
		#check if the index is close to beginning
		if (ind > (riffLength*2)):
			before = curChant[ind-(riffLength*2):ind]
		else:
			before = curChant[:ind]
		#check if the index is close to end
		endInd = ind + len(middleRiff)
		if (endInd < len(curChant) - (riffLength*2)):
			after = curChant[(endInd):endInd+(riffLength*2)]
		else:
			after = curChant[(endInd):]
		#print("Chant: ", i[0], " Mode: ", i[1])
		#print(before)
		#print(after + '\n')

		#check if we can cross words
		if (crossingwords):
			before = before.replace('.','')
			after = after.replace('.','')
			before = before[-riffLength:]
			after = after[:riffLength]
			#print(before + " \n" + after)
		#if not crossing words
		else:
			#split up the words and take the closest word
			before = before.split('.')
			after = after.split('.')
			before = before[len(before)-1]
			after = after[0]
			before = before[-riffLength:]
			after = after[:riffLength]
			#print(before + " \n" + after)
		
		beforeList.append((i[0],i[1],before))	
		afterList.append((i[0],i[1],after))		

#for the print function. Give the riff and the before or after list
def SortByMode(riff, BorAList):
	returnarray = [0,0,0,0,0,0,0,0,0]

	#total up instances
	for i in (BorAList):
		if (i[2] == riff):
			returnarray[i[1]-1] += 1
	#make the array percentages of total
	totalsum = sum(returnarray)
	for i in range(len(returnarray)):
		returnarray[i] = round(((returnarray[i]/totalsum)*100), 1)
	return returnarray

def PerByMode(riff, BorAList):
	returnarray = [0,0,0,0,0,0,0,0,0]
	totalmode = [0,0,0,0,0,0,0,0,0]
	#total up instances
	for i in (BorAList):
		totalmode[i[1]-1] += 1
		if (i[2] == riff):
			returnarray[i[1]-1] += 1
	#make the array percentages of total
	for i in range(len(returnarray)):
		if (totalmode[i] > 0):
			returnarray[i] = round(((returnarray[i]/totalmode[i])*100), 1)
		else:
			returnarray[i] = 0
	return returnarray

def printStats(beforeRiffStats, afterRiffStats, beforeList, afterList, riff):
	print("'"+riff+"' found", len(beforeList),"times")
	print("BEFORE: ")
	for i in range(len(beforeRiffStats)):
		percentage = round(beforeRiffStats[i][1]/len(beforeList)* 100, 2)
		print (i+1," Riff '"+beforeRiffStats[i][0]+"' appears",beforeRiffStats[i][1],"times ||", percentage, "%")
		print("All appearances: ",SortByMode(beforeRiffStats[i][0], beforeList))
		print("By mode:         ",PerByMode(beforeRiffStats[i][0], beforeList))
	print("AFTER: ")
	for i in range(len(afterRiffStats)):
		percentage = round(afterRiffStats[i][1]/len(afterList)* 100, 2)
		print (i+1," Riff '"+afterRiffStats[i][0]+"' appears",afterRiffStats[i][1],"times ||", percentage, "%")
		print("All appearances: ",SortByMode(afterRiffStats[i][0], afterList))
		print("By mode:         ",PerByMode(afterRiffStats[i][0], afterList))

def printStatsToFile(beforeRiffStats, afterRiffStats, beforeList, afterList, riff):
	f.write(riff+'\n')
	f.write(str(len(beforeList))+'\n')
	f.write("BEFORE:\n")
	for i in range(len(beforeRiffStats)):
		percentage = round(beforeRiffStats[i][1]/len(beforeList)* 100, 2)
		f.write(str(beforeRiffStats[i][0]) +',' +str(beforeRiffStats[i][1])+','+ str(percentage) + '%\n')
		f.write(str(SortByMode(beforeRiffStats[i][0], beforeList))+' , ')
		f.write(str(PerByMode(beforeRiffStats[i][0], beforeList))+'\n')
	f.write("AFTER:\n")
	for i in range(len(afterRiffStats)):
		percentage = round(afterRiffStats[i][1]/len(afterList)* 100, 2)
		f.write(str(afterRiffStats[i][0])+','+str(afterRiffStats[i][1])+','+ str(percentage)+ "%\n")
		f.write(str(SortByMode(afterRiffStats[i][0], afterList))+' , ')
		f.write(str(PerByMode(afterRiffStats[i][0], afterList))+'\n')
	f.write('N\n')
######## START OF MAIN SCRIPT ########
def main(riff):
	for i in chantList:
		CheckBeforeAndAfter(i, riff)

	#extract the licks to count
	newBefore = []
	newAfter = []
	checkArray = []
	for i in range(len(beforeList)):
		newBefore.append(beforeList[i][2])
		newAfter.append(afterList[i][2])

		if (beforeList[i][2] == 'mno'):
			checkArray.append(beforeList[i])

	beforeRiffStats = collections.Counter(newBefore).most_common(numberOfResults)
	afterRiffStats = collections.Counter(newAfter).most_common(numberOfResults)

	toReturn = {}
	for i in range(len(afterRiffStats)):
		toReturn[afterRiffStats[i][0]] = PerByMode(afterRiffStats[i][0], afterList)
	######## PRINTING ########
	printStats(beforeRiffStats,afterRiffStats, beforeList,afterList, riff)
	printStatsToFile(beforeRiffStats,afterRiffStats, beforeList,afterList, riff)
	beforeList.clear()
	afterList.clear()

	return toReturn

def CHANTBOT(start, mode):
	newchant = start
	riff = start
	lastriff = ''
	#temp for mode 1
	startchoices = ['c','d','e','f','g','h']
	for i in range(40):
		afterStats = main(riff)

		#making the dict of percentages
		percArr = []
		total = 0
		for r in afterStats:
			perc = afterStats[r][mode-1]
			if (perc > 0):
				total += math.ceil(perc)
				percArr.append([r,total])

		#get the random number in the range and find the result
		rando = random.randint(1,total+1)

		nextriff = ''
		for i in percArr:
			if (rando <= i[1]):
				nextriff = i[0]
				break

		if (nextriff != '' ):
			newchant += '-' + nextriff
			#to add more here
			a = newchant.split('---')
			nextriff = a[len(a)-1].replace('-','')
			if (len(nextriff) > 3):
				nextriff = nextriff[-3:]
			#print(nextriff)
			#print(percArr)
			riff = nextriff
		elif(lastriff != ''):
			newchant += '--'
			riff = startchoices[random.randint(0,5)]
		
		lastriff = nextriff
		print(newchant)




#random number, anything on or below the percArr percentage

######## START OF SCRIPT ######## 'Ba','aB','bc','cb','ef','fe','Jh', 'hJ', 'jk','kj', 'mn','nm'
inputRiff = ['Ba','aB','bc','cb','ef','fe','Jh', 'hJ', 'jk','kj', 'mn','nm']
mode = 1
AddToChantList()
#CHANTBOT(inputRiff[0], mode)
f = open("demofile3.txt", "w")
for r in inputRiff:
	main(r)
	print('\n\n\n')
f.write('END')
f.close()


