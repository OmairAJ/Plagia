#!/usr/bin/env python
## indexMap.py

import os
import sys
import string
import MySQLdb
import argparse


## Casefold text
def casefold(text):
	text = text.lower()
	text = text.translate(string.maketrans("",""), string.punctuation)
	text = text.split()
	text = filter(None, text)
	return text

## Patterned combination list
## much more easier ways to do this discovered
# Solution 1
# def combo(w, l):
#     lst = []
#     for i in range(len(w)):
#         if l == 1:
#             lst.append(w[i])
#         for c in combo(w[i+1:], l-1):
#             lst.append(w[i] + c)
#     return lst
# Solution 2
# from itertools import combinations
# list(combinations(range(5),3)
# or just use the overly complicated one below
def keyPattern(keyList, patternSize, startPosition, endPosition, flag):
	if patternSize == 0:
		return ['']
	keys = []
	# this code is pretty messed up
	# need to clean it and
	# fix the words start and end
	# positions calculation/processing
	for i in range(len(keyList)):
		j = 0
		k = 0
		subKeys = keyPattern(keyList[i + 1:], patternSize - 1, startPosition, endPosition, False)
		for subKey in subKeys:
			key = ''
			key = keyList[i]
			if (len(subKey) > 0):
				key += '_'
			key += subKey
			if k == 3:
				j = 1
				k += 0
			endPosition = startPosition + patternSize + j - 1
			if flag:
				j += 1
				k += 1
				keyI = [key, startPosition, endPosition, jDocument]
			else:
				keyI = key
			keys.append(keyI)
	return keys

## Generate n-grams
def genNGrams(wordList, windowSize, overlapSize, patternSize, fileName):
	nGrams = []
	for i in range(len(wordList) - (windowSize - (windowSize - overlapSize))):
		nGram  = keyPattern(wordList[i:i + windowSize], patternSize, i, i + windowSize, True)
		for j in range(len(nGram)):
			nGrams.append(nGram[j])
	return nGrams


## Command-line arguments parser
parser = argparse.ArgumentParser(description='Index documents for contextual n-grams based plagiarism detection.')
parser.add_argument('-j', action='store',   dest='Job', type=str, help='Job identifier')
parser.add_argument('-v', action='version', version='%(prog)s 1.0')
parserResults = parser.parse_args()

## Initialise
jIdentifier  = parserResults.Job
jDocument  =  ''
jPath      =  ''
jWindow    =  0
jOverlap   =  0
jPattern   =  0
jStatus    =  ''

## Update mySQL with current status
try:
	db = MySQLdb.connect('127.0.0.1', 'plagiaAdminDb', 'fty5687gjh8T776HFf87UG78567jg7sq', 'plagiaDB')
except Exception as e:
	sys.exit('Unable to connect to the database.')

cursor = db.cursor()
cursor.execute('SELECT * FROM jobs')
result = cursor.fetchall()

if result:
	for att in result:
		if att[1] == jIdentifier:
			jPath      =  att[2]
			jDocument  =  att[3]
			jWindow    =  int(att[6])
			jOverlap   =  int(att[7])
			jPattern   =  int(att[8])
			jStatus    =  att[9]

cursor.execute('UPDATE jobs SET jStatus=%s WHERE jIdentifier=%s', ('Indexing', jIdentifier))
db.commit()

## Open document and read
documentRead = open(jPath + jDocument, 'r')
wordstring = documentRead.read()
wordList = casefold(wordstring)

## Process word lists
documentNGrams = genNGrams(wordList, jWindow, jOverlap, jPattern, jDocument)

## Output results
for i in range(0, len(documentNGrams)):
	print '%s\t1\t(%s, %s, %s)\t%s' % (documentNGrams[i][0], documentNGrams[i][1], documentNGrams[i][2], documentNGrams[i][3], jIdentifier)

## Update status
cursor.execute('UPDATE jobs SET jStatus=%s WHERE jIdentifier=%s', ('Index Mapped', jIdentifier))
db.commit()
