import os
from datetime import datetime
import socket
import sys
import numpy as np

sys.path.append('/Users/dijin/OneDrive/OneDrive - umich.edu/Tools')
from tools import *
from tools_temporal import *


def write_subset_by_time(input_file_path, output_file_path):

	time_lower_str = '2016-01-01T00:00:00'
	time_upper_str = '2016-06-30T23:59:59'
	

	fOut = open(output_file_path, 'w')

	tools_temporal = Tools_temporal()
	tools_temporal.subset_time(input_file_path, fOut, time_lower_str, time_upper_str)

	fOut.close()

	return



if __name__ == '__main__':

	if len(sys.argv) != 3:
		sys.exit('<usage:> <input_dir_path> <output_file_path>')


	input_file_path = sys.argv[1]
	output_file_path = sys.argv[2]

	get_year(input_file_path, output_file_path)

