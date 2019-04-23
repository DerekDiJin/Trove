import sys
import os
import datetime
from pathlib import Path



if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit('usage: time_id_anonymizer.py input_file_path')

	input_file_path = sys.argv[1]
	c = '\t'
	time_l_str = '2018-01-01T00:00:00'
	time_u_str = '2018-10-01T00:00:00'
	time_l = datetime.datetime.strptime(time_l_str, "%Y-%m-%dT%H:%M:%S")
	time_u = datetime.datetime.strptime(time_u_str, "%Y-%m-%dT%H:%M:%S")
	
	src_file_path = sys.argv[0]
	cur_dir = str(Path().resolve())
	output_file_path = cur_dir + '/' + input_file_path.split('/')[-1][:-4] + '_anonymized.tsv'
	map_file_path = cur_dir + '/' + input_file_path.split('/')[-1][:-4] + '_lookup.tsv'
	
	print(input_file_path)
	print(output_file_path)
	print(map_file_path)

	container = set([])
	OLD_NEW_ID_DICT = {}


	fIn = open(input_file_path, 'r')
	lines = fIn.readlines()

	counter = 0
	for line in lines:
		counter += 1
		if counter % 100000 == 0:
			print(counter)

# 		if (line[0].isnumeric() == False):
# 			continue

		parts = line.strip('\r\n').split(c)
		src_orig = parts[0]
		dst_orig = parts[1]
		time_str = parts[2][:-6]

		time_v = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")

		if time_v <= time_u and time_v >= time_l:

			container.add(src_orig)
			container.add(dst_orig)


	fIn.close()

	OLD_NEW_ID_DICT = dict(zip(list(container), range(len(container))))


	fOut = open(output_file_path, 'w')
	fIn = open(input_file_path, 'r')
	lines = fIn.readlines()

	counter = 0
	for line in lines:
		counter += 1
		if counter % 100000 == 0:
			print(counter)

		parts = line.strip('\r\n').split(c)
		src_orig = parts[0]
		dst_orig = parts[1]
		time_str = parts[2][:-6]

		time_v = datetime.datetime.strptime(time_str, "%Y-%m-%dT%H:%M:%S")

		if time_v <= time_u and time_v >= time_l:

			src_new = OLD_NEW_ID_DICT[src_orig]
			dst_new = OLD_NEW_ID_DICT[dst_orig]

			fOut.write(str(src_new) + '\t' + str(dst_new) + '\t' + time_str + '\n')


	fIn.close()
	fOut.close()

	fOut = open(map_file_path, 'w')
	for k,v in OLD_NEW_ID_DICT.items():
		fOut.write(str(k) + '\t' + str(v) + '\n')


	fOut.close()