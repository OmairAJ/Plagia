#indexReduce.py
# python indexReduce.py -s -d text.m

import os
import sys
import string
import argparse
import fileinput


## Casefold text
def casefold(text):
	text = text.lower()
	text = text.translate(string.maketrans("",""), string.punctuation)
	text = text.split()
	text = filter(None, text)
	return text

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

##  Command-line arguments parser
parser = argparse.ArgumentParser(description="Index documents for contextual n-grams based plagiarism detection. Only text files with .m extension are accepted for indexing.")

parser.add_argument("-d",  action="store",      dest="Document", type=str, help="Document to index")
parser.add_argument("-s",  action="store_true", dest="Source",   help="This is a source document")
parser.add_argument("-v",  action="version",    version="%(prog)s 1.0")

parserResults = parser.parse_args()

documentOpen  = parserResults.Document
documentType  = parserResults.Source

if documentType:
	documentFolder = "sources/"
else:
	documentFolder = "users/"

if (documentOpen is None):
	print "This application requires an index file with .m extesion to function."
	print "\n"
	sys.exit()
else:
	documentPath = os.path.dirname(documentOpen)
	documentName = casefold(os.path.splitext(os.path.basename(documentOpen))[0])[0]
	documentExtension = casefold(os.path.splitext(os.path.basename(documentOpen))[1])[0]
	documentFile = documentName + "." + documentExtension

	if documentExtension != "m":
		print "This application only accepts plain text files with .m extension."
		print "\n"
		sys.exit()

	documentRead = open(documentOpen, "r")
	indexList = documentRead.readlines()

words = []
counts = []
positions = []
keys = []
uniqueKeys = []

for i in range (len(indexList)):
	line = indexList[i].strip()
	word, count, position = line.split('\t', 2)
	key = [word, count, position]
	keys.append(key)

uniqueKeys = removeDuplicates(keys)

documentSavePath = "indexes/" + documentFolder

if not os.path.exists(documentSavePath): os.makedirs(documentSavePath)
documentExport = open(documentSavePath + documentName + ".n","w")

for i in range(0, len(uniqueKeys)):
	documentExport.write("%s\t%s\t%s\n" % (uniqueKeys[i][0], uniqueKeys[i][1], uniqueKeys[i][2]))
	print "%s\t%s\t%s" % (uniqueKeys[i][0], uniqueKeys[i][1], uniqueKeys[i][2])

documentExport.close()

