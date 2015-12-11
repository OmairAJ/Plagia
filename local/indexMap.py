#indexMap.py
# python indexMap.py -s -d test.txt

import os
import sys
import math
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

## Number of combinations
# combinations(windowSize, patternSize)
def combinations(n, s):
	return math.factorial(n) / (math.factorial(s) * math.factorial(n-s))

## Pattern list
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
			key = ""
			key = keyList[i]
			if (len(subKey) > 0):
				key += "_"
			key += subKey
			if k == 3:
				j = 1
				k += 0
			endPosition = startPosition + patternSize + j - 1
			if flag:
				j += 1
				k += 1
				keyI = [key, startPosition, endPosition, documentFile]
			else:
				keyI = key
			keys.append(keyI)
	return keys

## Generate n-grams
def genNGrams(wordList, windowSize, overlapSize, fileName):
	nGrams = []
	for i in range(len(wordList) - (windowSize - (windowSize - overlapSize))):
		nGram  = keyPattern(wordList[i:i + windowSize], patternSize, i, i + windowSize, True)
		for j in range(len(nGram)):
			nGrams.append(nGram[j])
	return nGrams

## Command-line arguments parser
parser = argparse.ArgumentParser(description="Index documents for contextual n-grams based plagiarism detection. Only text files with .txt extension are accepted for indexing.")

parser.add_argument("-d", action="store",      dest="Document", type=str, help="Document to index")
parser.add_argument("-w", action="store",      dest="Window",   type=int, default=5, help="Window size for index")
parser.add_argument("-o", action="store",      dest="Overlap",  type=int, default=4, help="Overlap size for index")
parser.add_argument("-p", action="store",      dest="Pattern",  type=int, default=3, help="Pattern size for index")
parser.add_argument("-s", action="store_true", dest="Source",   help="This is a source document")
parser.add_argument("-v", action="version",    version="%(prog)s 1.0")

parserResults = parser.parse_args()

documentOpen  = parserResults.Document
windowSize    = parserResults.Window
overlapSize   = parserResults.Overlap
patternSize   = parserResults.Pattern
documentType  = parserResults.Source

if documentType:
	documentFolder = "sources/"
else:
	documentFolder = "users/"

## Checks
if windowSize == 0:
	print "The window size must be greater than 0."
	print "\n"
	sys.exit()

if overlapSize == 0:
	print "The overlap size must be greater than 0."
	print "\n"
	sys.exit()

if patternSize == 0:
	print "The pattern size must be greater than 0."
	print "\n"
	sys.exit()

if (documentOpen is None):
	print "This application requires at least one text file with .txt extesion to function."
	print "\n"
	sys.exit()
else:
	documentPath = os.path.dirname(documentOpen)
	documentName = casefold(os.path.splitext(os.path.basename(documentOpen))[0])[0]
	documentExtension = casefold(os.path.splitext(os.path.basename(documentOpen))[1])[0]
	documentFile = documentName + "." + documentExtension

	if documentExtension != "txt":
		print "This application only accepts plain text files with .txt extension."
		print "\n"
		sys.exit()

	documentRead = open(documentOpen, "r")
	wordstring = documentRead.read()


# Apply casefolding to the text from the document
wordList = casefold(wordstring)

documentNGrams = genNGrams(wordList, windowSize, overlapSize, documentFile)

documentSavePath = "maps/" + documentFolder

if not os.path.exists(documentSavePath): os.makedirs(documentSavePath)
if not os.path.exists("documents/" + documentFolder): os.makedirs("documents/" + documentFolder)

os.system ("cp %s %s" % (documentOpen, "documents/" + documentFolder + documentFile))
documentExport = open(documentSavePath + documentName + ".m","w")

for i in range(0, len(documentNGrams)):
	documentExport.write("%s\t1\t(%s, %s, %s)\n" % (documentNGrams[i][0], documentNGrams[i][1], documentNGrams[i][2], documentNGrams[i][3]))
	print "%s\t1\t(%s, %s, %s)" % (documentNGrams[i][0], documentNGrams[i][1], documentNGrams[i][2], documentNGrams[i][3])

documentExport.close()

