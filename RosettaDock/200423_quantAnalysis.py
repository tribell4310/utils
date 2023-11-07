"""
23 April 2020

This script will do I-score vs. RMSD analysis for ALL outputs of a Rosetta docking output.
Crystal structure (relaxed and with built hydrogens) must be in the root directory with the script.
Must specify a subdirectory that contains the score.sc file and the output pdb files.

Missing dependency - I'm going to split this across 2 functions.  This is the server-side function and does
the computation-intensive mathy bits.  Statistics should also be done here.  Second function I run locally, it does the plotting.

"""

import sys
import math
import os
import csv
import cPickle as pickle


def main(inCrystal, inPath):
	# Populate a dictionary structure with I-score and RMSD
	pdbList = []
	for root, dirs, files in os.walk("./"+inPath):
		for filename in files:
			if filename[-4:] == ".pdb":
				pdbList.append([int(filename[-8:-4]), filename])
	
	I_scores = getIScores(inPath+"/score.sc")
	pdbScores = {}

	for i in xrange(0, len(pdbList)):
		rootMean = rmsdWrapper(inCrystal, inPath+"/"+pdbList[i][1])
		print pdbList[i][0], rootMean, (-1*I_scores[i])
		pdbScores[pdbList[i][0]] = {"rootMean":rootMean, "ISc":(-1*I_scores[i])}

	# Dump to pickle - end of server-side functions
	with open(inPath+'.pickle', 'wb') as h:
		pickle.dump(pdbScores, h, protocol=pickle.HIGHEST_PROTOCOL)
	h.close()


def rmsdWrapper(inCrystal, inDock):
	# Read in files, convert to atom dictionaries
	f = open(inCrystal, "r")
	g = open(inDock, "r")
	crystDict = resortToDict(f.readlines())
	dockDict = resortToDict(g.readlines())
	
	# Build an object to correlate dictionary references
	dictCorr = corrDicts(crystDict, dockDict, debugFlag=False)

	# Calculate RMSDs
	rootMean = rmsd(crystDict, dockDict, dictCorr)
	return rootMean

def corrDicts(dict1, dict2, debugFlag):
	holder = []
	for cAtom in dict1:
		modFlag = False
		for dAtom in dict2:
			# Same chain?
			if dict1[cAtom]['Chain'] == dict2[dAtom]['Chain']:
				if dict1[cAtom]['ResiID'] == dict2[dAtom]['ResiID']:
					if dict1[cAtom]['Residue'] == dict2[dAtom]['Residue']:
						if dict1[cAtom]['Element'] == dict2[dAtom]['Element']:
							holder.append([cAtom, dAtom])
							modFlag = True
							break
		if debugFlag == True:
			if modFlag == False:
				print "No match found:", cAtom, dict1[cAtom]

	if debugFlag == True:
		for item in holder:
			if dict1[item[0]]['Element'] != dict2[item[1]]['Element']:
				print item, dict1[item[0]], dict2[item[1]]
		print "The following are non-unique mappings (slow for large files):"
		for h in xrange(0,2):
			for i in xrange(0, len(holder)):
				for j in xrange(0, len(holder)):
					if i != j:
						if holder[i][0] == holder[j][0]:
							print "Non-unique mapping:", h, i, j, holder[i], holder[j]
		print "Done scanning for non-unique mappings."

	return holder

def extractParts(line):
	AtomID = int(line[6:11].strip())
	AtomName = line[12:16].strip()
	Residue = line[17:20].strip()
	Chain = line[21].strip()
	ResiID = int(line[22:26].strip())
	xCoord = float(line[30:38].strip())
	yCoord = float(line[38:46].strip())
	zCoord = float(line[46:54].strip())
	return [AtomID, AtomName, Residue, Chain, ResiID, xCoord, yCoord, zCoord]

def resortToDict(inLines):
	newDict = {}
	for line in inLines:
		if line[0:4] == "ATOM":
			items = extractParts(line)
			newDict[items[0]] = {'Residue':items[2], 'Chain':items[3], 'ResiID':items[4], "xCoord":items[5], "yCoord":items[6], "zCoord":items[7], "Element":items[1]}
	return newDict

def rmsd(dict1, dict2, corrList):
	dists = []
	for i in xrange(0, len(corrList)):
		dist_i = calcDist(dict1[corrList[i][0]], dict2[corrList[i][1]])
		dists.append(dist_i)

	sum_of_square_dist = 0
	for i in xrange(0, len(dists)):
		sum_of_square_dist += (dists[i])**2
	return math.sqrt((1.0/len(dists))*sum_of_square_dist)

def calcDist(atomI, atomJ):
	# Directly accepts an entry from atomDict
	x1 = atomI['xCoord']
	y1 = atomI['yCoord']
	z1 = atomI['zCoord']
	x2 = atomJ['xCoord']
	y2 = atomJ['yCoord']
	z2 = atomJ['zCoord']
	return math.sqrt(((x1-x2)**2)+((y1-y2)**2)+((z1-z2)**2))

def getIScores(inFile):
	with open(inFile, "r") as csvfile:
		my_vals = csv.reader(csvfile, delimiter=" ", quotechar="|")
		strip_vals = []
		for val in my_vals:
			holder = []
			for i in xrange(0, len(val)):
				if val[i] != "":
					holder.append(val[i])
			strip_vals.append(holder)

	out_vals = []
	for j in xrange(2, len(strip_vals)):
		out_vals.append(float(strip_vals[j][5]))

	return out_vals


if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "Script requires exactly 3 argument.  Usage: python foo.py inCrytal.pdb inPath"
		exit()

	main(sys.argv[1], sys.argv[2])