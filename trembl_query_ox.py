"""

trembl_query_ox.py
Tristan Bell, Mass General Hospital

Matches a list of OX ID's to a very large fasta file.
Outputs a fasta file with the matches and a csv spreadsheet correlating OX/OS/sequence.

For uniprot trembl, takes about 2hr and 600 GB of memory to run.

"""


import sys
from Bio import SeqIO
import subprocess


def main(inAcc, inFasta):
	# Load the accessions into a list
	queries = []
	with open(inAcc, "r") as f:
		lines = f.readlines()
	for line in lines:
		queries.append(line.strip().replace(",", ""))
	
	print("Uniprot trembl contains ~226m entries")
	print("Total user queries:\t"+str(len(queries)))

	# Load the whole thing to memory as dictionary, storing ox, id, seq separately, key indexed by ox -> header
	record_dict = {}
	records = SeqIO.parse(inFasta, "fasta")
	for record in records:
		ox = parse_header(str(record.description))
		if ox == False:
			continue # if a sequence header doesn't have an ox label, this will stop it from breaking
		if ox not in record_dict:
			record_dict[ox] = {}
		record_dict[ox][str(record.id)] = str(record.seq)
		
	print("done loading!")

	# Scan queries and write out
	print("\nWriting out fasta and csv files...")
	with open(no_ext(inAcc)+"_out.fasta", "w") as g:
		with open(no_ext(inAcc)+"_out.csv", "w") as h:
			for query in queries:
				sub_dict = record_dict[query]
				for item in sub_dict:
					this_seq = str(record_dict[query][item])
					g.write(">"+query+"_"+item+"\n"+this_seq+"\n")
					h.write(query+","+item+","+this_seq+"\n")
	print("Done with everything!\n\nThis python script tends to hang after completion.\nIf you're seeing this message, it's safe to manually kill your python process!")


def parse_header(inStr):
	ox_loc = inStr.find("OX=")
	if ox_loc == -1:
		return False
	else:
		space_loc = inStr.find(" ", ox_loc)
		return inStr[ox_loc+3:space_loc]


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
	if len(sys.argv) == 3:
		main(sys.argv[1], sys.argv[2])
	else:
		print("Check usage: trembl_query_ox.py inOxList inFasta(trembl)")