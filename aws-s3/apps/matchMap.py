#!/usr/bin/env python
## matchMap.py

import os
import sys
import string
import MySQLdb
import argparse


##  Command-line arguments parser
parser = argparse.ArgumentParser(description='Match documents for contextual n-grams based plagiarism detection.')
parser.add_argument('-j', action='store',   dest='Job', type=str, help='Job identifier')
parser.add_argument('-v', action='version', version='%(prog)s 1.0')
parserResults = parser.parse_args()

## Initialise
jIdentifier   = parserResults.Job
indexPath = 'indexes/'

jPath      =  ''
jDocument  =  ''
jWindow    =  0
jOverlap   =  0
jPattern   =  0
jStatus    =  ''

keys = []

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

cursor.execute('UPDATE jobs SET jStatus=%s WHERE jIdentifier=%s', ('Matching', jIdentifier))
db.commit()

## Go through folder and read each file
for itemName in os.listdir(indexPath):
	# Loops over each itemName in the path. Joins the path and the itemName
	# and assigns the value to itemName.
	itemName = os.path.join(indexPath, itemName)

	## Read file lines
	if os.path.isfile(itemName):
		indexList = file(itemName, 'r').readlines()
		for i in range (len(indexList)):
			line = indexList[i].strip()
			word, count, meta = line.split('\t', 2)
			key = [word, count, meta]
			keys.append(key)
	
## Output results
for i in range(0, len(keys)):
	print '%s\t%s\t%s\t%s' % (keys[i][0], keys[i][1], keys[i][2], jIdentifier)

## Update status
cursor.execute('UPDATE jobs SET jStatus=%s WHERE jIdentifier=%s', ('Match Mapped', jIdentifier))
db.commit()
