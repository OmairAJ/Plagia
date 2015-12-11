#matchReduce.py
# python matchReduce.py -d text.m

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
parser.add_argument("-v",  action="version",    version="%(prog)s 1.0")

parserResults = parser.parse_args()

documentOpen  = parserResults.Document

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
	indexList = sorted(documentRead.readlines())

keys = []
metas = []

current_word = None
current_count = 0
current_meta = []
word = None

documentSavePath = "matches/"
if not os.path.exists(documentSavePath): os.makedirs(documentSavePath)
documentExport = open(documentSavePath + documentName + ".txt","w")

for i in range (len(indexList)):
	line = indexList[i].strip()
	word, count, meta = line.split('\t', 2)

	try:
		count = int(count)
	except ValueError:
		continue

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

if current_word == word:
	if current_count > 1:
		key = [current_word, current_count, current_meta]
		keys.append(key)

for i in range (len(keys)):
	for j in range (len(keys[i][2])):
		documentMeta = uniqifier(casefold(keys[i][2][j].replace('txt', '')))
		if documentName == documentMeta[2]:
			print '%s\t%s\t%s' % (keys[i][0], keys[i][1], keys[i][2])
			documentExport.write('%s\t%s\t%s\n' % (keys[i][0], keys[i][1], keys[i][2]))

documentExport.close()

