
import datetime
import socket
import sys
import numpy as np

from tools import *


def write_mapping(OLD_NEW_DICT, input_file_path):

	output_file_path = input_file_path.split('/')[-1].split('.')[-2] + '_lookup.tsv'
	fOut = open(output_file_path, 'w')

	for old_id in OLD_NEW_DICT:
		newline = old_id + '\t' + str(OLD_NEW_DICT[old_id]) + '\n'
		fOut.write(newline)

	fOut.close()

	return



if __name__ == '__main__':

	if len(sys.argv) != 3:
		sys.exit('<usage:> <input_graph_file_path> <input_nodes_selected_file_path>')

	T = 560


	input_graph_file_path = sys.argv[1]
	input_nodes_selected_file_path = sys.argv[2]

	tools = Tools()

	delimiter = tools.get_delimiter(input_graph_file_path)


	id_count_dict, count_id_dict = tools.read_lookup(input_nodes_selected_file_path)


	fOut = open('Trove_depth_aggre.tsv', 'w')
	fIn = open(input_graph_file_path, 'r')

	for line in fIn.readlines():

		src, dst, wei = line.strip().split('\t')

		if (src in id_count_dict.keys()) or (dst in id_count_dict.keys()):
			fOut.write(line)


	fIn.close()
	fOut.close()

