import os
from datetime import datetime
import socket
import sys
import numpy as np

sys.path.append('/Users/dijin/OneDrive/OneDrive - umich.edu/Tools')
from tools import *


def remove_self_comm(input_file_path, output_file_path):

	fOut = open(output_file_path, 'w')

	fIn = open(input_file_path, 'r')
	for line in fIn.readlines():
		src_str, dst_str, time_str = line.strip().split('\t')
		if src_str == dst_str:
			continue
		new_line = line
		fOut.write(new_line)

	fIn.close()
	fOut.close()

	return



if __name__ == '__main__':

	if len(sys.argv) != 3:
		sys.exit('<usage:> <input_dir_path> <output_file_path>')


	input_file_path = sys.argv[1]
	output_file_path = sys.argv[2]

	remove_self_comm(input_file_path, output_file_path)

