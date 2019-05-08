import os
from datetime import datetime
import socket
import sys
import numpy as np
from collections import defaultdict

sys.path.append('/Users/dijin/OneDrive/OneDrive - umich.edu/Tools')
from tools import *


def parse_file(cur_filename, fOut):

	fIn = open(cur_filename, 'r')

	for line in fIn.readlines():
		if 'find' in line or 'moved' in line:
			continue
		else:
			fOut.write(line)


	fIn.close()


	return



if __name__ == '__main__':

	if len(sys.argv) != 3:
		sys.exit('<usage:> <input_dir_path> <output_file_path>')


	input_dir_path = sys.argv[1]
	output_file_path = sys.argv[2]

	

	fOut = open(output_file_path, 'w')

	for filename in os.listdir(input_dir_path):
		print filename
		cur_file_path = input_dir_path + '/' + filename
		parse_file(cur_file_path, fOut)

	

	fOut.close()




