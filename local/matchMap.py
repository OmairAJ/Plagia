#matchMap.py
# python matchMap.py -d test.n

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

## Command-line arguments parser
parser = argparse.ArgumentParser(description="Match indexes for contextual n-grams based plagiarism detection. Only text files with .n extension are accepted for matching.")

parser.add_argument("-d", action="store",      dest="Document", type=str, help="Document to match against sources")
parser.add_argument("-v", action="version",    version="%(prog)s 1.0")

parserResults = parser.parse_args()

documentOpen  = parserResults.Document

## Checks
if (documentOpen is None):
	print "This application requires at least one text file with .n extesion to function."
	print "\n"
	sys.exit()
else:
	documentPath = os.path.dirname(documentOpen)
	documentName = casefold(os.path.splitext(os.path.basename(documentOpen))[0])[0]
	documentExtension = casefold(os.path.splitext(os.path.basename(documentOpen))[1])[0]
	documentFile = documentName + "." + documentExtension

	if documentExtension != "n":
		print "This application only accepts plain text files with .n extension."
		print "\n"
		sys.exit()

	documentRead = open(documentOpen, "r")
	userIndexList = documentRead.readlines()

keys = []

pathSources = "indexes/sources/"

documentSavePath = "bigindexes/"
if not os.path.exists(documentSavePath): os.makedirs(documentSavePath)
documentExport = open(documentSavePath + documentName + ".m","w")

for itemName in os.listdir(pathSources):
	#Loops over each itemName in the path. Joins the path and the itemName
	#and assigns the value to itemName.
	itemName = os.path.join(pathSources, itemName)

	if os.path.isfile(itemName):
		sourceIndexList = file(itemName, 'r').readlines()
		for i in range (len(sourceIndexList)):
			line = sourceIndexList[i].strip()
			word, count, meta = line.split('\t', 2)
			key = [word, count, meta]
			keys.append(key)

for i in range (len(userIndexList)):
	line = userIndexList[i].strip()
	word, count, meta = line.split('\t', 2)
	key = [word, count, meta]
	keys.append(key)
	
for i in range(0, len(keys)):
	documentExport.write("%s\t%s\t%s\n" % (keys[i][0], keys[i][1], keys[i][2]))
	print "%s\t%s\t%s" % (keys[i][0], keys[i][1], keys[i][2])


documentExport.close()

