import os
from datetime import datetime
import socket
import sys
import numpy as np
from collections import defaultdict

sys.path.append('/Users/dijin/OneDrive/OneDrive - umich.edu/Tools')
from tools import *
from tools_temporal import *





if __name__ == '__main__':

	if len(sys.argv) != 4:
		sys.exit('<usage:> <input_nodes_selected_file> <input_intro_year_file_path> <output_file_path>')


	input_nodes_selected_file = sys.argv[1]
	input_intro_year_file_path = sys.argv[2]
	output_file_path = sys.argv[3]

	tools = Tools()
	nodes_selected_dict, nodes_selected_dict_r = tools.lookup_col1_col2(input_nodes_selected_file)
	nodes_selected_set = set(nodes_selected_dict.keys())

	neighbors_dict = defaultdict(int)
	
	fIn = open(input_intro_year_file_path, 'r')

	for line in fIn.readlines():
		node1, node2, node3, time_str = line.strip().split('\t')
		if node1 not in nodes_selected_set:
			neighbors_dict[node1] += 1
		if node2 not in nodes_selected_set:
			neighbors_dict[node2] += 1
		if node3 not in nodes_selected_set:
			neighbors_dict[node3] += 1


	fIn.close()



	fOut = open(output_file_path, 'w')

	for node in neighbors_dict:
		new_line = node + '\t' + str(neighbors_dict[node]) + '\n'
		fOut.write(new_line)

	fOut.close()
