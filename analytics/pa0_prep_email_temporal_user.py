import json
import codecs
import os
import numpy as np
import sys
from collections import defaultdict


if len(sys.argv) != 2:
	sys.exit('usage: <input_file_path>')

input_file_path = sys.argv[1]
# directory_output = 'email_to_titile_group_by_company_p/'

temporal_dict = defaultdict(set)

fIn = open(input_file_path, 'r')
lines = fIn.readlines()

counter = 0
for line in lines:

	if counter % 100000 == 0:
		print counter
	counter += 1

	src, dst, time = line.strip('\r\n').split('\t')
	day = time.split('T')[0][5:]
	temporal_dict[day].add(src)

# print temporal_dict
fIn.close()

output_file_path = 'email_temporal_dict.tsv'
fOut = open(output_file_path, 'w')

for ele in temporal_dict:
	new_line = str(ele) + '\t' + str( len(temporal_dict[ele]) ) + '\n'
	fOut.write(new_line)

fOut.close()