#!/usr/bin/env python
## indexReduce.py

import os
import sys
import string
import MySQLdb
import fileinput


## Remove duplicate n-grams
def removeDuplicates(keyList):
	keys = []
	uniques = []
	uniqueNGrams = []
	uniqueNGrams2 = []

	for i in range(len(keyList)):
		keys.append(keyList[i][0])

	uniques = uniqifier(keys)

	for i in range(len(keyList)):
		for j in range(len(uniques)):
			if (keyList[i][0] == uniques[j]):
				uniqueNGrams.append(keyList[i])

	uniqueNGrams = sorted(uniqueNGrams)
		
	for i in range(len(uniqueNGrams)):
		if i+1 < len(uniqueNGrams):
			if (uniqueNGrams[i][0] == uniqueNGrams[i+1][0]):
				flag = True
			else:
				flag = False

		if flag == False:
			uniqueNGrams2.append(uniqueNGrams[i])

	return uniqueNGrams2

## Generate unique values from list
## http://www.peterbe.com/plog/uniqifiers-benchmark
def uniqifier(seq, idfun=None):
	if idfun is None:
		def idfun(x): return x
	seen = {}
	result = []
	for item in seq:
		marker = idfun(item)
		if marker in seen: continue
		seen[marker] = 1
		result.append(item)
	return result


## Set variables
documentSavePath = 'indexes/'

jIdentifier = None
jPath      =  ''
jDocument  =  ''
jWindow    =  0
jOverlap   =  0
jPattern   =  0
jStatus    =  ''

keys       = []
uniqueKeys = []

## Recieve lines
for line in sys.stdin:
	line = line.strip()
	word, count, position, jIdentifier = line.split('\t', 3)
	key = [word, count, position]
	keys.append(key)

## Retrive mySQL data about current job and update status
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

cursor.execute('UPDATE jobs SET jStatus=%s WHERE jIdentifier=%s', ('Index Reducing', jIdentifier))
db.commit()

## Sort, clean up and reduce
uniqueKeys = removeDuplicates(keys)

## Export document
# documentExport = open(documentSavePath + jDocument, 'w')

## Output results
for i in range(0, len(uniqueKeys)):
	print '%s\t%s\t%s' % (uniqueKeys[i][0], uniqueKeys[i][1], uniqueKeys[i][2])
	#documentExport.write('%s\t%s\t%s\n' % (uniqueKeys[i][0], uniqueKeys[i][1], uniqueKeys[i][2]))

# documentExport.close()

## Update status
cursor.execute('UPDATE jobs SET jStatus=%s WHERE jIdentifier=%s', ('Indexed', jIdentifier))
db.commit()
