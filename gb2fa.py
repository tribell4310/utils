"""

gb2fa.py

Convert all genbank files in subdirectory genbank into fasta files in subdirectory fasta.

"""


import sys
import os
from os import listdir
from os.path import isfile, join
from Bio import SeqIO


def main():
	# Check for the genbank and fasta subdirectories
	if os.path.isdir(join(os.getcwd(), "fasta")) == False:
		os.mkdir(join(os.getcwd(), "fasta"))
	if os.path.isdir(join(os.getcwd(), "genbank")) == False:
		print("\nNo genbank folder in this directory. Exiting.")
		exit()

	# Read and validate files in the genbank subdirectory.
	onlyfiles = [f for f in listdir(join(os.getcwd(), "genbank")) if isfile(join(os.getcwd(), "genbank", f))]
	valfiles = []
	for eachfile in onlyfiles:
		if eachfile.endswith(".gb") or eachfile.endswith(".gbk"):
			valfiles.append(eachfile)
	if len(valfiles) == 0:
		print("\nNo valid genbank files (suffix .gb or .gbk) detected in genbank folder. Exiting.")
		exit()

	# Test
	print(len(valfiles))

	# Fasta conversion loop
	for eachfile in valfiles:
		with open(join(os.getcwd(), "genbank", eachfile), "r") as f:
			with open(join(os.getcwd(), "fasta", no_ext(eachfile)+".fasta"), "w") as g:
				for seq_record in SeqIO.parse(f, "genbank"):
					g.write(">"+no_ext(eachfile)+"\n"+str(seq_record.seq)+"\n")


def no_ext(inStr):
	"""
	Takes an input filename and returns a string with the file extension removed.
	"""
	prevPos = 0
	currentPos = 0
	while currentPos != -1:
		prevPos = currentPos
		currentPos = inStr.find(".", prevPos+1)
	return inStr[0:prevPos]


if __name__ == "__main__":
	if len(sys.argv) != 1:
		print("This script takes no arguments.  Exiting.")
		exit()
	else:
		main()