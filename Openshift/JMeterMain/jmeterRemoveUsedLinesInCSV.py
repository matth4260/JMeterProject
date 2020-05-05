import sys
import os
import csv


def removeLinesInFile(csvName, filesPath):
	usedLinesFileName = csvName + "UsedLines.txt"
	with open(filesPath + csvName + '.csv', 'r') as fin, open(filesPath + csvName + 'WithoutUsedLines.csv', 'w') as fout:
		writer = csv.writer(fout)

		usedLines = open(filesPath + usedLinesFileName, 'r',encoding='utf-8').readlines()

		for csvRow in csv.reader(fin):
			used = False
			for usedLine in usedLines:
				if (csvRow[0] + '\n') == usedLine:
					used = True
					break
			if not(used):
				writer.writerow(csvRow)
                    
DIR = "/Users/leanovia/Downloads/"

listOfCSV = []

for file in os.listdir(DIR):
	if file.endswith("UsedLines.txt"):
		fileName = file[0:-13]
		removeLinesInFile(fileName, DIR)
		os.remove(DIR + file)
		os.remove(DIR + fileName + ".csv")
		os.rename(DIR + fileName + "WithoutUsedLines.csv", DIR + fileName + ".csv")

