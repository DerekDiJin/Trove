import os
from datetime import datetime
import socket
import sys
import numpy as np

from tools import *


def parse_file(cur_filename, fOut):

	time_upper_str = '2016-12-31T23:59:59'
	time_lower_str = '2016-01-01T00:00:00'

	time_upper = datetime.datetime.strptime(time_upper_str,'%Y-%m-%dT%H:%M:%S')
	time_lower = datetime.datetime.strptime(time_lower_str,'%Y-%m-%dT%H:%M:%S')

	fIn = open(cur_filename, 'r')

	for line in fIn.readlines():
		try:
			src_str, dst_str, time_str, type_str = line.strip().split('\t')
			cur_time = datetime.datetime.strptime(time_str[:-6],'%Y-%m-%dT%H:%M:%S')

			if cur_time > time_lower and cur_time < time_upper :
				new_line = src_str + '\t' + dst_str + '\t' + time_str + '\n'
				fOut.write(new_line)

		except:
			print 'Error:\t' + cur_filename + '\t' + line


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

