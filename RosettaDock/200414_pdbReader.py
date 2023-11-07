"""
14 April 2020

This is a generalized pdb atom reader script, because pdb file format sucks.
"""

import sys


def main():
	collateList = []
	#fileList = ["model_new_dom1.pdb", "model_new_dom2.pdb", "model_new_dom3.pdb", "model_new_dom4.pdb"]
	#fileList = ["200416_dom1_aligned.pdb", "200416_dom2_aligned.pdb"]
	fileList = ["TempPymolSessions/B3.pdb", "TempPymolSessions/B4.pdb"]
	#fileList = ["200416_5dzv_pcdh21_m_d1b.pdb", "200416_5dzv_pcdh21_m_d2b.pdb"]

	# Read in all the lists, only accepting atoms
	for myFile in fileList:
		openFile = open(myFile, "r")
		lines = openFile.readlines()
		for line in lines:
			if line[0:4] == "ATOM":
				collateList.append(line)
	
	# Build an atom matrix
	atoms = []
	for j in xrange(0, len(collateList)):
		atoms.append(extractParts(collateList[j]))

	# Renumber duplicated atoms
	renumAtoms = []
	renumAtoms.append(atoms[0])
	for j in xrange(1, len(atoms)):
		if int(atoms[j][1].strip()) == int(atoms[j-1][1].strip()) + 1:
			renumAtoms.append(atoms[j])
		else:
			# Modify all adjacent lines
			linediff = int(atoms[j-1][1]) - int(atoms[j][1]) + 1
			for i in xrange(j, len(atoms)):
				atoms[i][1] = leftpad((int(atoms[i][1]) + linediff), 5)
			renumAtoms.append(atoms[j])
	
	# Rename all units to chain "A"
	for atom in renumAtoms:
		if atom[5] != "A":
			atom[5] = "A"

	# Output to a writer
	f = open("TempPymolSessions/B34.pdb", "w")
	for atom in renumAtoms:
		f.write(recombineParts(atom))
	f.write("END")
	f.close()


def extractParts(inLine):
	recordName = inLine[0:6]
	atomNum = inLine[6:11]
	atomName = inLine[12:16]
	altLoc = inLine[16]
	resiName = inLine[17:20]
	chainID = inLine[21]
	resiNum = inLine[22:26]
	insCode = inLine[26]
	x = inLine[30:38]
	y = inLine[38:46]
	z = inLine[46:54]
	occ = inLine[54:60]
	bf = inLine[60:66]
	elem = inLine[76:78]
	charge = inLine[78:80]
	return [recordName, atomNum, atomName, altLoc, resiName, chainID, resiNum, insCode, x, y, z, occ, bf, elem, charge]


def recombineParts(a):
	outStr = a[0]+a[1]+" "+a[2]+a[3]+a[4]+" "+a[5]+a[6]+a[7]+"   "+a[8]+a[9]+a[10]+a[11]+a[12]+"          "+a[13]+a[14]+"\n"
	# Check string integrity
	if len(outStr) != 81:
		print "ACK!", outStr
	return outStr


def leftpad(inInt, strLen):
	inStr = str(inInt)
	for b in xrange(0, strLen+1):
		if len(inStr) != strLen:
			inStr = " "+inStr
	return inStr


if __name__ == '__main__':
	#Pass filename argument to main function
	if len(sys.argv) != 1:
		print "Script requires exactly 1 argument.  Usage: python foo.py"
		exit()
	
	main()