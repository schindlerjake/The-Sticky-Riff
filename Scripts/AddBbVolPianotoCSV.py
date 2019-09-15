import pandas as pd
import numpy as np
import csv
import re

chantList = []
CSV_DATA = pd.read_csv("../Data/CHNT_DATA.csv");
newchantlist = []
checkIndexs = []




abaAndFalse = [64, 189, 314, 319, 335, 367, 404, 480, 481, 569, 608, 628, 633, 664, 671, 862, 913, 914, 915, 928, 929, 930, 931, 932, 934, 943, 949, 1042, 1046, 1256, 1287, 1290, 1291, 1379, 1430, 1577, 1578, 1585, 1586, 1593, 1615, 1925, 1933, 2394, 2395, 2435, 2438, 2446, 2448, 2449, 2508, 2559, 2609, 2613, 2790, 2808, 2838, 2839, 2842, 2843, 3120, 4079, 4256, 4325, 4368, 4464]
bccNoflats = [60, 66, 230, 244, 246, 315, 336, 361, 398, 472, 536, 687, 704, 1007, 1220, 1509, 1533, 1534, 1536, 1740, 1767, 1799, 1872, 1880, 1898, 1902, 2195, 2456, 2464, 2465, 2576, 2592, 2606, 2671, 2693, 2753, 3695, 3787, 4534, 5162, 5164, 5499]
abaAndFlase = {4610, 9, 4106, 19, 20, 2083, 38, 1064, 5676, 1584, 49, 2100, 53, 5686, 579, 1604, 5708, 4686, 5712, 1109, 1621, 89, 1114, 1115, 92, 1626, 5724, 5727, 3185, 114, 2164, 2174, 640, 1153, 2178, 3202, 1672, 4232, 2187, 1683, 1692, 670, 2206, 674, 5796, 5797, 5288, 1715, 2740, 181, 182, 5313, 4803, 204, 718, 719, 1742, 2260, 2773, 1238, 216, 2780, 2783, 4323, 1768, 2801, 2805, 2813, 2814, 1279, 5885, 2315, 2828, 1815, 3863, 282, 283, 5403, 1829, 2861, 3374, 4397, 304, 307, 4921, 1342, 4930, 1861, 838, 839, 329, 2890, 1358, 1369, 1388, 1390, 1400, 2938, 1914, 1926, 920, 5538, 3504, 4530, 4030, 450, 451, 1475, 2010, 2523, 1002, 4601, 4606}

volpiano ='9abcdefghjklmnopqrs'
hughes   ='%*-0123456789><;'


#takes a char that has been verified to be a hughes char and returns the valid volpiano char
#based on the offset (calculated by mode and final below)
def charToVol(char, offset):
	if (char == '%'):
		return volpiano[offset-4]
	elif (char == '*'):
		return volpiano[offset-3]
	elif (char == '-'):
		return volpiano[offset-2]
	elif (char == '>'):
		return volpiano[offset+9]
	elif (char == '<'):
		return char
	elif (char == ';'):
		return char
	else:
		return volpiano[(int(char) -1) + offset]


def replaceWithFlat(word):
	newword = ''
	erase = False
	for i in range(len(word)):
		if (erase):
			erase = False
		elif (word[i] == '<'):
			erase = True
		elif (word[i] == 'b'):
			newword += 'yb'
		elif (word[i] == 'j'):
			newword += 'ij'
		else:
			newword += word[i]	
	return newword

#RULES:
#if a flat appears in a word, any b after that flat in that word is flattened
#if chant starts with < then all are flatted (pg176)
def addFlats(chant, mode, index):
	chantArr = chant.split('---')
	returnArr = []
	flag = False
	count = 0

	#if the first character of the chant is < then flatten every b
	if (chantArr[0][0] == '<'):
		if ('b' in chantArr[0] or 'j' in chantArr[0]):
			#checkIndexs.append(index)
			True;
		for word in (chantArr):
			newword = ''
			newword += replaceWithFlat(word)
			returnArr.append(newword)
	
	#otherwise....

	else:
		change = False	
		for word in (chantArr):
			newword = ''
			if ('<' in word or change):
				change = True
				#check for hexachord (note: low b is assumed always in the hexachord until ';')
				#just looking for it to go past an 'e'(volpaino 'm')
				#this may not catch every case (for example in a d hexachord, but most examples I found made this a non issue and a reasonable solution)
				if ('m' in word and 'j' in word and '<' not in word):
					change = False
				if (change):
					#erase used to erase the extra '-' when < is found
					erase = False
					for i in range(len(word)):
						if (erase):
							erase = False
						elif (word[i] == 'b'):
							newword += 'yb'
						elif (word[i] == 'j'):
							newword += 'ij'
						elif (word[i] == ';'):
							change = False
							newword += word[i]
						elif (word[i] == '<'):
							erase = True
						else:
							newword += word[i]

					returnArr.append(newword)
				else:
					returnArr.append(word)
			else:
				returnArr.append(word)

			'''
			if ('<' in word):
				#reset the flag if we didn't find anything before another sign
				if (flag):
					flag = False
				#checks to see if there's a flat sign but no b
				#if so, turns the flag to true which will look to the next word
				if ('j' not in word and 'b' not in word):	
					flag = True
				newword += word[:word.find('<')]
				newword += replaceWithFlat(word[word.find('<')+2:])
			elif (flag):
				flag = False
				newword += replaceWithFlat(word)

			else:
				newword = word
			returnArr.append(newword)'''

	returnStr = ''

	#clean up some formmatting before returning
	for i in range(len(returnArr)-1):
		returnStr += returnArr[i] + '---'
	if (returnStr[0] == '-'):
		returnStr = returnStr[1:]
	returnStr = returnStr.replace('------', '---')
	return returnStr

#checks to see if a-b-a phrase is in a D hexicord and should be flattened 
def abaFlatInsert(chant, index, mode):
	chantArr = chant.split('---')
	returnArr = []
	for i in range(len(chantArr)):
		newword = ''
		if ('h-j-h' in chantArr[i]):
			#countSigns will count how many tests to see if the b should be flat
			#I'll deal with it at the end of this if statement 
			countSigns = 0

			#NEW TEST 1: no go’s for h-j-h-k and k-h-j-h then no flat
			if ('k-h-j-h' in chantArr[i] or 'h-j-h-k' in chantArr[i]):
				countSigns = 10
			#Auto flat d-h-j-h
			if ('d-h-j-h' in chantArr[i] and mode == 1 or mode == 2):
				countSigns = -20
			#TEST 1.5: is there a 'c','d', or 'e' above in the same word 
			if ((mode == 1 or mode == 2) and ('k' in chantArr[i] or 'l' in chantArr[i] or 'm' in chantArr[i])):
				countSigns = 3
			if ((mode == 5 or mode == 6) and ('m' in chantArr[i])):
				countSigns = 3
			
			#FACTORS IN FLATTENING H-J-H
			if (i == 0):
				if ((mode == 1 or mode == 2) and ('k' in chantArr[i+1] or 'l' in chantArr[i+1] or 'm' in chantArr[i+1])):
					countSigns += 2
				if ((mode == 5 or mode == 6) and ('m' in chantArr[i+1])):
					countSigns += 2				
			elif (i == len(chantArr)-2):
				countSigns += 1
				if ((mode == 1 or mode == 2) and ('k' in chantArr[i-1] or 'l' in chantArr[i-1] or 'm' in chantArr[i-1])):
					countSigns += 2
				if ((mode == 5 or mode == 6) and ('m' in chantArr[i-1])):
					countSigns += 2				
			elif (mode == 1 or mode ==2):
				if ('k' in chantArr[i+1] or 'l' in chantArr[i+1] or 'm' in chantArr[i+1]):
					countSigns += 2
				if ('k' in chantArr[i+2] or 'l' in chantArr[i+2] or 'm' in chantArr[i+2]):
					countSigns += 1
				if ('k' in chantArr[i-1] or 'l' in chantArr[i-1] or 'm' in chantArr[i-1]):
					countSigns += 2
				if ('k' in chantArr[i-2] or 'l' in chantArr[i-2] or 'm' in chantArr[i-2]):
					countSigns += 1
			elif (mode == 5 or mode == 6):
				if ('m' in chantArr[i+1] or 'm' in chantArr[i-1]):
					countSigns += 2
				if ('m' in chantArr[i+2] or 'm' in chantArr[i-2]):
					countSigns += 1
			
			#THIS IS FINE ADD THE FLAT!!!
			if (countSigns <= 4):
				for c in range(len(chantArr[i])):
					if (chantArr[i][c] == 'j' and chantArr[i][c-2] == 'h' and c == (len(chantArr[i]) -1 ) ):
						newword += chantArr[i][c]
					elif (chantArr[i][c] == 'j' and chantArr[i][c-2] == 'h' and chantArr[i][c+2] == 'h'):
						newword += 'ij'
					else:
						newword += chantArr[i][c]

			else:
				newword = chantArr[i]
				if (countSigns < 10):
					#print ("Index:", index,"Mode:", mode,"Word:", newword)
					True 	

			returnArr.append(newword)	
		else:
			returnArr.append(chantArr[i])

	returnStr = ''
	for i in range(len(returnArr)-1):
		returnStr += returnArr[i] + '---'
	return returnStr


def bccFlatInsert(chant,index,flag):
	#don't care about the flag anymore
	if (True):
		chantArr = chant.split('---')
		returnArr = []
		for word in chantArr:
			newword = ''
			if ('b-c-c' in word):
				#find the index of all the b-c-c's in the word
				index = [m.start() for m in re.finditer('(?=b-c-c)', word)]
				for i in range(len(word)):
					#if the phrase is b-c-c
					if (word[i] == 'b' and (i == 0 or word[i-1] == '-') and word[i+2] == 'c' and word[i+4] == 'c'):
						if (word[i-1] != 'y'):
							newword += 'yb'
						else:
							newword += word[i]
					#if there is a b and it's close to the galican cadence (dashes are an extra character)
					elif (word[i]=='b'):
						for ind in index:
							howFar = 10 #10 = 5 characters
							if ((i+howFar >= ind) or (i-howFar-4 <= ind)):
								if (word[i-1] != 'y'):
									newword += 'yb'
								else:
									newword += word[i]
								
							else:
								newword +=word[i]
					else: 
						newword +=word[i]
			else:
				newword = word
			returnArr.append(newword)

		returnStr = ''
		for i in range(len(returnArr)-1):
			returnStr += returnArr[i] + '---'
		return returnStr
	#if there are no flats written, check there. There are 42
	else:
		return chant

def finalCheck(newchant, index):
	chantArr = newchant.split('---')
	returnArr = []

	#triggers all b's to be converted in the hexachord until a break
	change = False
	for word in chantArr:
		newword = ''
		if ('ij' in  word or change):
			change = True
			#predict for new hexachord
			if (mode == 1 or mode == 2):
				if ('k' in word or 'l' in word):
					change = False
			if (mode == 5 or mode == 6):
				if ('l' in word or 'm' in word):
					change = False

			if (change):
				for i in range(len(word)):
					if (word[i] == 'j' and (i == 0 or word[i-1] == '-')):
						if (word[i-1] != 'i'):
							newword += 'ij'
						else:
							newword += word[i]
					elif (word[i] == ';'):
						change = False
						newword += word[i]
					else:
						newword += word[i]

				returnArr.append(newword)
			else:
				returnArr.append(word)
		else:
			returnArr.append(word)
	#Look through again to see all h-ij-h and correct any b's before it (currently rule 8)
	#similar to code in yB expand
	for i in range(len(returnArr)):
		if ('h-ij-h' in returnArr[i]):
			#change all the b's to b flats until the end of a phrase in both directions
			z = 1
			break1 =  True #going backward
			break2 = True #going forwards
			if (";" in returnArr[i]):
				break2 = False
			while ((i-z >= 0 and i+z < len(returnArr)) and (break1 or break2)):
				if (break1):
					if (";" in returnArr[i-z]):
						break1 = False
					if ((mode == 1 or mode == 2) and ("k" in returnArr[i-z] or "l" in returnArr[i-z])):
						break1 = False
					if ((mode == 5 or mode == 6) and ("l" in returnArr[i-z] or "m" in returnArr[i-z])):
						break1 = False
					elif ("-j" in returnArr[i-z]):
						#print (index, returnArr[i-z])
						returnArr[i-z] = returnArr[i-z].replace('j', 'ij')
						#print(returnArr[i-z])
						#print(returnArr[i])
				if (break2):
					if ((mode == 1 or mode == 2) and ("k" in returnArr[i+z] or "l" in returnArr[i+z])):
						break2 = False
					elif ((mode == 5 or mode == 6) and ("l" in returnArr[i+z] or "m" in returnArr[i+z])):
						break2 = False
					elif ("-j" in returnArr[i+z]):
						print (index, returnArr[i+z])
						returnArr[i+z] = returnArr[i+z].replace('j', 'ij')
						print(returnArr[i+z])
						print(returnArr[i])
					if (";" in returnArr[i+z]):
						break2 = False					
				z += 1




	returnStr = ''
	for i in range(len(returnArr)-1):
		returnStr += returnArr[i] + '---'
	return returnStr

def ybExpand(newchant, index):
	returnArr = newchant.split('---')

	for i in range(len(returnArr)):
		if ('yb' in returnArr[i]):
			#change all the b's to b flats until the end of a phrase in both directions
			z = 1
			break1 =  True #going backward
			break2 = True #going forwards
			if (";" in returnArr[i]):
				break2 = False
			while ((i-z >= 0 and i+z < len(returnArr)) and (break1 or break2)):
				if (break1):
					if (";" in returnArr[i-z]):
						break1 = False
					elif ("-b" in returnArr[i-z]):
						#print (index, returnArr[i-z])
						returnArr[i-z] = returnArr[i-z].replace('b', 'yb')
						#print(returnArr[i-z])
						#print(returnArr[i])
				if (break2):
					if (";" in returnArr[i+z]):
						break2 = False
					if ("-b" in returnArr[i+z]):
						#print (index, returnArr[i+z])
						returnArr[i+z] = returnArr[i+z].replace('b', 'yb')
						#print(returnArr[i+z])
						#print(returnArr[i])
				z += 1
	
	returnStr = ''
	for i in range(len(returnArr)-1):
		returnStr += returnArr[i] + '---'
	return returnStr

def fixOffDuplicates(newchant, index, duplicates):
	returnArr = newchant.split('---')
	for dup in duplicates:
		flag = False
		winningWord = ''
		for ind in dup:
			for checkInd in dup:
				if (returnArr[ind] != returnArr[checkInd]):
					#take the longer one (because we know that must have been changed)
					if (len(returnArr[ind]) > len(returnArr[checkInd])):
						winningWord = returnArr[ind]
					else:
						winningWord = returnArr[checkInd]
					flag = True
		if (flag):
			#print (index)
			#print (winningWord)
			#print(returnArr)
			for ind in dup:
				returnArr[ind] = winningWord
			#print(returnArr)

	returnStr = ''
	for i in range(len(returnArr)-1):
		returnStr += returnArr[i] + '---'
	return returnStr

#returns an array where each index is an array of word locations of duplicates ex [[2,3],[5,10]]
def getDup(chant):
	chant = chant.replace("<-", "")
	chant = chant.replace(";-", "")
	chantArr = chant.split('---')
	duplicateReturn = set()
	for word in chantArr:
		dups = []
		for i in range(len(chantArr)):
			if (word == chantArr[i]):
				dups.append(i)
		if (len(dups) > 1):
			duplicateReturn.add(tuple(dups))

	return (duplicateReturn)


def onList(index):
	if (index in abaAndFalse or index in bccNoflats or index in abaAndFlase):
		return True

	return False


#######################################
############### MAIN ##################
#######################################

for index, row in CSV_DATA.iterrows():
	#if (index == 1167):
		try:
			chant = row['Chantwords']
			mode = row['Mode'].strip("'")
			if (mode != '?'):
				mode = int(mode)
			flag = row['Flat']
			final = row['Final']
			chantList.append([index, mode, final, chant, flag])
		except Exception as e: print(e)

for i in chantList:

	#replace chars and prep chant (ends with END, each word seperated by a single space)
	chant = i[3]

	chant = chant.replace('$','')
	chant = chant.replace('^','')
	chant = chant.replace('  ',' ')
	chant = chant.replace(' < ',' <')
	chant = chant.replace(' \()','END')


	#put each chant into volpiano with <

	#grab data
	index = i[0]
	mode = i[1]
	final = i[2]
	flag = i[4]

	offset = 4
	if (mode == 1 or mode == 2):
		if (final == 'a'):
			offset += 4
		elif (final == 'g'):
			offset += 3
	elif (mode == 3 or mode == 4):
		offset += 1
		if (final == 'a'):
			offset +=3
	elif (mode == 5 or mode == 6):
		offset += 2	
		if (final == 'c' or final == 'C'):
			offset -=3
	elif (mode == 7 or mode == 8):
		offset += 3	
		if (final == 'a'):
			offset +=1
		elif (final == 'c'):
			offset -= 4
	elif (mode == '?'):
		if (final == 'a'):
			offset+=4
		elif (final == 'g'):
			offset+=3
		elif (final == 'c'):
			offset -= 1

	chant = chant.split()
	newchant = ''
	for j in range(len(chant)):
		newword = ''
		for char in chant[j]:
			if (char in hughes):
				char = charToVol(char, offset)
				newword +=char + '-'
		if (newword != ''):
			newchant += newword + "--"

	#newchant is now a string of volpiano chars with < for flats, words seperated by '---'
	Hugheschant = newchant
	#get duplicates for finalCheck
	duplicates = getDup(newchant)

	#add flats shown in manuscript	
	if (flag):
		newchant = addFlats(newchant, mode, index);


	#check for aba motion and send off to check the hexacord.
	if (('h-j-h' in newchant) and (mode == 2 or mode == 1 or mode == 5 or mode == 6)):
		newchant = abaFlatInsert(newchant, index, mode)	
	if (('-b-c-c' in newchant) and (mode == 6 or mode == 5 or final == 'c')):
		newchant = bccFlatInsert(newchant, index, flag)
	if ('-j' in newchant):
		if (mode == 2 or mode == 1 or mode == 5 or mode == 6):
			newchant = finalCheck(newchant, index)
	if ('yb' in newchant):
		newchant = ybExpand(newchant, index)

	newchant = newchant.replace(";-", "")
	if ("-b" in newchant or "-j" in newchant):
		newchant = fixOffDuplicates(newchant, index, duplicates)



	newchantlist.append((mode, Hugheschant, newchant, flag));

labels = ['Mode', 'Hugheschant', 'FlatVolPiano', 'Flag']
df = pd.DataFrame.from_records(newchantlist, columns = labels)
df.to_csv("TempData2.CSV", sep=',')






