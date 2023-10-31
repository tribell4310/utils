"""

json2bfactor.py

Convert AF2 json containing plddt scores into list of bfactors.

"""


import sys
import json


def main(inJson):
	with open(inJson, "r") as f:
		# Load json
		data = json.load(f)

		# Write out a new file with just the lddt scores
		with open(no_ext(inJson)+"_lddt.txt", "w") as g:
			for i in range(0, len(data["plddt"])):
				if i != len(data["plddt"]) - 1:
					g.write(str(data["plddt"][i] / 100)+"\n")
				else:
					g.write(str(data["plddt"][i] / 100))


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
	if len(sys.argv) != 2:
		print("Requires one argument.")
	else:
		main(sys.argv[1])