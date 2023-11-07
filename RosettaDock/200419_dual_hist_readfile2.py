"""
19 April 2020

This script makes nice overlaid histograms for my group meeting presentation on 21 April.

Tasks:
 - Load in some data structure
 - Get the outputs to look how I want them
 - Normalize?
 - Print

"""

import numpy as np
import matplotlib.pyplot as plt
import csv
plt.style.use('seaborn-deep')


my_vals_float_pos = []
my_vals_float_neg = []

# Read in the csv data file
with open('200422_dom1.csv', 'r') as csvfile:
	my_vals = csv.reader(csvfile, delimiter=',', quotechar='|')

	# Create a "global" array of float vals
	for item in my_vals:
		my_vals_float_pos.append(float(str(item[0])))
		my_vals_float_neg.append(float(str(item[1])))

print max(my_vals_float_pos), max(my_vals_float_neg)
#print max(my_vals_float_1523), max(my_vals_float_1521), max(my_vals_float_2121)

#x = np.random.normal(1, 2, 5000)
#y = np.random.normal(-1, 3, 2000)
bins = np.linspace(0, 45, 16)

#plt.hist([x, y], bins, label=['x', 'y'])
plt.hist([my_vals_float_pos, my_vals_float_neg], bins, label=['Pos', 'Neg'])
plt.legend(loc='upper right')
plt.xlabel('Interaction Score')
plt.ylabel('Frequency')
plt.title('5DZV 1-Domain Interaction')
#plt.show()
plt.savefig('200422_dom1_pos_neg.png', dpi=400, facecolor='w', edgecolor='w')