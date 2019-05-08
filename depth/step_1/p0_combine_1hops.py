import os
from datetime import datetime
import socket
import sys
import numpy as np
from collections import defaultdict

sys.path.append('/Users/dijin/OneDrive/OneDrive - umich.edu/Tools')
from tools import *


def parse_file(cur_filename, node_count_dict):

	fIn = open(cur_filename, 'r')

	for line in fIn.readlines():
		src, dst, time, marker = line.strip().split('\t')
		node_count_dict[src] += 1
		node_count_dict[dst] += 1


	fIn.close()


	return



if __name__ == '__main__':

	if len(sys.argv) != 3:
		sys.exit('<usage:> <input_dir_path> <output_file_path>')


	input_dir_path = sys.argv[1]
	output_file_path = sys.argv[2]

	

	node_count_dict = defaultdict(int)

	for filename in os.listdir(input_dir_path):
		print filename
		cur_file_path = input_dir_path + '/' + filename
		parse_file(cur_file_path, node_count_dict)

	fOut = open(output_file_path, 'w')

	for ele in node_count_dict:

		new_line = ele + '\t' + str(node_count_dict[ele]) + '\n'
		fOut.write(new_line)

	fOut.close()




