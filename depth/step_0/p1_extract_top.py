
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
		sys.exit('<usage:> <input_file_path> <lookup_file_path>')

	T = 560


	input_file_path = sys.argv[1]
	lookup_file_path = sys.argv[2]

	tools = Tools()

	delimiter = tools.get_delimiter(input_file_path)
	adj = tools.get_lil_matrix(input_file_path)
	out_deg_dict, in_deg_dict = tools.get_deg_dict(adj)

	sorted_out_deg_dict = sorted(out_deg_dict.items(), key=lambda kv: kv[1], reverse=True)
	nodes_selected = sorted_out_deg_dict[:T]
	print nodes_selected

	old_new_dict, new_old_dict = tools.read_lookup(lookup_file_path)


	fOut = open('nodes_selected.tsv', 'w')

	for node_s in nodes_selected:
		id_new = new_old_dict[str(node_s[0])]
		new_line = id_new + '\t' + str(node_s[1]) + '\n'

		fOut.write(new_line)

	fOut.close()

