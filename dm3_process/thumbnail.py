"""
thumbnail.py

This script takes a set of images in a subdirectory called "test", rescales them, and outputs them within the same directory.

"""

import sys
import os
from os import listdir
from os.path import isfile, join
from PIL import Image

def main():
	# Get the list of extant autopick files
	#onlyfiles = [f for f in listdir("./images/") if isfile(join("./images/", f))]
	onlyfiles = [f for f in listdir("./test/") if isfile(join("./test/", f))]
	#print(onlyfiles)

	my_quality = 2
	for each_file in onlyfiles:
		im = Image.open("./test/"+each_file)
		im.thumbnail((341,480))
		im.save("./test/"+no_ext(each_file)+"_res"+str(my_quality)+".jpg")


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
	main()