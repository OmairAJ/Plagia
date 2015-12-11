#!/usr/bin/env python
## matchReduce.py

import os
import sys
import string
import MySQLdb
import fileinput


## Casefold text
def casefold(text):
	text = text.lower()
	text = text.translate(string.maketrans("",""), string.punctuation)
	text = text.split()
	text = filter(None, text)
	return text

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


## Initialise
documentSavePath = 'matches/'

jIdentifier = None
jPath      =  ''
jDocument  =  ''
jWindow    =  0
jOverlap   =  0
jPattern   =  0
jStatus    =  ''

keys  = []
metas = []

word = None
count = 0
meta = None

current_word  = None
current_count = 0
current_meta  = []

## Recieve lines
for line in sys.stdin:
	line = line.strip()
	word, count, meta, jIdentifier = line.split('\t', 3)

	## Convert count to integer
	try:
		count = int(count)
	except ValueError:
		continue

	## Do some counting by matching
	if current_word == word:
		current_count += count
		current_meta.append(meta)
	else:
		if current_word:
			if current_count > 1:
				key = [current_word, current_count, current_meta]
				keys.append(key)
		current_count = count
		current_word = word
		current_meta = [meta]

## And the last one
if current_word == word:
	if current_count > 1:
		key = [current_word, current_count, current_meta]
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

cursor.execute('UPDATE jobs SET jStatus=%s WHERE jIdentifier=%s', ('Match Reducing', jIdentifier))
db.commit()

## Export document
# documentExport = open(documentSavePath + str(jIdentifier) + '.txt', 'w')

## Output results
for i in range (len(keys)):
	for j in range (len(keys[i][2])):
		documentMeta = uniqifier(casefold(keys[i][2][j].replace('txt', '')))
		if casefold(jDocument.replace('txt', ''))[0] == documentMeta[2]:
			print '%s\t%s\t%s' % (keys[i][0], keys[i][1], keys[i][2])
			# documentExport.write('%s\t%s\t%s\n' % (keys[i][0], keys[i][1], keys[i][2]))

# documentExport.close()

## Update status
cursor.execute('UPDATE jobs SET jStatus=%s, jDocumentResult=%s WHERE jIdentifier=%s', ('Matched', documentSavePath + str(jIdentifier) + '.txt', jIdentifier))
db.commit()
