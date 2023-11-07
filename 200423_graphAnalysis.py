"""
23 April 2020

This is the second half of the quantitative analysis script.  It runs locally and does graphical plotting
using calculations done by 200423_quantAnalysis.py on the server side.


"""

import sys
import cPickle as pickle
import matplotlib.pyplot as plt
import numpy as np

def main(inCrystal, outName, inPickleList):
	# Iteratively open and merge inPickleList into a single dictionary
	for j in xrange(0, len(inPickleList)):
		tempHold = open(inPickleList[j], 'rb')
		if j == 0:
			pdbScores = pickle.load(tempHold)
			arbName = inPickleList[j][:-7]
		else:
			temp = pickle.load(tempHold)
			pdbScores = mergeDicts(pdbScores, temp)
	
	# Generate and write out scatterplots at different percentiles
	for item in [0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05]:
		plotter(pdbScores, arbName, outName, item)

	# Generate cutoff plot - what fraction of I-scores represent top 2.5% of RMSDs?
	optCutoff(pdbScores, arbName, outName)

	# Write out to a csv file
	writeOut(pdbScores, arbName)

def plotter(inDict, inPdb, outName, thresh):
	# Make linked lists out of the dictionary
	ISc = []
	rmsd = []
	for item in inDict:
		ISc.append(inDict[item]["ISc"])
		rmsd.append(inDict[item]["rootMean"])
		#print inDict[item]["rootMean"], inDict[item]["ISc"]

	# Identify points in N% for rmsd
	rmsd_select = percentileScore(rmsd, False, thresh)
	ISc_select = percentileScore(ISc, True, thresh)

	# Invert for 1 / RMSD
	inv_rmsd = []
	for i in xrange(0, len(rmsd)):
		inv_rmsd.append(1/rmsd[i])

	# Define the axis boundaries
	xmax = ((int(max(inv_rmsd)) / 0.2)+1) * 0.2
	ymax = ((int(max(ISc)) / 5)+1) * 5

	# Define subsets for special coloration
	rmsd_blk = []
	rmsd_red = []
	rmsd_grn = []
	rmsd_blu = []
	ISc_blk = []
	ISc_red = []
	ISc_grn = []
	ISc_blu = []

	# Assign colors
	for i in xrange(0, len(rmsd_select)):
		if rmsd_select[i] == 0:
			if ISc_select[i] == 0:
				rmsd_blk.append(inv_rmsd[i])
				ISc_blk.append(ISc[i])
			elif ISc_select[i] == 1:
				rmsd_blu.append(inv_rmsd[i])
				ISc_blu.append(ISc[i])
		elif rmsd_select[i] == 1:
			if ISc_select[i] == 0:
				rmsd_grn.append(inv_rmsd[i])
				ISc_grn.append(ISc[i])
			elif ISc_select[i] == 1:
				rmsd_red.append(inv_rmsd[i])
				ISc_red.append(ISc[i])

	# Plot out
	fig, ax = plt.subplots()
	ax.scatter(rmsd_blk, ISc_blk, color="black", s=11)
	ax.scatter(rmsd_blu, ISc_blu, color="blue", s=11)
	ax.scatter(rmsd_grn, ISc_grn, color="green", s=11)
	ax.scatter(rmsd_red, ISc_red, color="red", s=11)
	ax.set(xlim=(0, xmax), ylim=(0, ymax))
	plt.title(outName+" (n="+str(max(inDict.keys()))+") - "+str(100*thresh)+" Percent Cutoff")
	plt.xlabel("1 / RMSD ( 1/ A)")
	plt.ylabel("Interaction Score")
	#plt.show()
	plt.savefig(inPdb+'_'+str(100*thresh)+'.png', dpi=400, facecolor='w', edgecolor='w')

def mergeDicts(baseDict, newDict):
	# THIS IS A HUGE GAPING HOLE THAT I NEED TO FILL IN SOON
	maxVal = max(baseDict.keys())
	maxNew = max(newDict.keys())
	newNewDict = {}
	for i in xrange(1, maxNew+1):
		baseDict[maxVal+i] = newDict[i]
	return baseDict

def percentileScore(inList, greaterLessFlag, thresh):
	# True flag => top N%; False flag => bottom N%
	sortList = sorted(inList)
	percentile = int(len(sortList)*thresh)
	if greaterLessFlag == False:
		cutoff = sortList[percentile]
	else:
		cutoff = sortList[len(sortList)-percentile]

	# Generate a list of flags
	flagList = []
	for i in xrange(0, len(inList)):
		if greaterLessFlag == False:
			if inList[i] <= cutoff:
				flagList.append(1)
			else:
				flagList.append(0)
		else:
			if inList[i] >= cutoff:
				flagList.append(1)
			else:
				flagList.append(0)

	return flagList

def writeOut(inDict, outName):
	f = open(outName+".csv", "wb")
	f.write("AggID,ISc,RMSD\r")
	for i in xrange(1, len(inDict.keys())+1):
		f.write(str(i)+","+str(inDict[i]["ISc"])+","+str(inDict[i]["rootMean"])+"\r")
	f.close()

def optCutoff(inDict, inPdb, outName):
	# Make linked lists out of the dictionary
	ISc = []
	rmsd = []
	for item in inDict:
		ISc.append(inDict[item]["ISc"])
		rmsd.append(inDict[item]["rootMean"])

	# Run percentiles every 0.5%
	x = []
	y = []
	rmsd_list = percentileScore(rmsd, False, 0.020)

	for i in xrange(1, 1000):
		x.append(i/10.0)
		ISc_list = percentileScore(ISc, True, (i/1000.0))
		mutualCounter = 0
		iCounter = 0
		for j in xrange(0, len(rmsd_list)):
			if rmsd_list[j] == 1:
				if ISc_list[j] == 1:
					mutualCounter += 1
			if ISc_list[j] == 1:
				iCounter += 1
		y.append(float(mutualCounter)/float(iCounter))

	# Plot out
	fig, ax = plt.subplots()
	ax.scatter(x, y, color="black", s=11)
	ax.set(xlim=(0.0, 10.0))
	plt.title(outName+" Threshholding Analysis")
	plt.xlabel("Percentage Cutoff")
	plt.ylabel("Correlated 98th Perc. RMSD, High I-Score per High I-Score")
	plt.savefig(inPdb+'_cutoffs.png', dpi=400, facecolor='w', edgecolor='w')


if __name__ == '__main__':
	if len(sys.argv) < 4:
		print "Script requires at least 4 arguments.  Usage: python foo.py inCrytal.pdb out_name first.pickle second.pickle ..."
		exit()

	pickleFork = []
	for i in xrange(3, len(sys.argv)):
		pickleFork.append(sys.argv[i])
	
	main(sys.argv[1], sys.argv[2], pickleFork)