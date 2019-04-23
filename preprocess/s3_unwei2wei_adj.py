import sys
import scipy.sparse as sps
import numpy as np

GLOBAL_EDGE_DICT = {}

def unwei2wei(input_graph_file_path):

	# counter = 0
	# output_file_path = input_graph_file_path.split('.')[0] + '_wei.tsv'
	# fOut = open(output_file_path, 'w')

	# fIn = open(input_graph_file_path, 'r')
	# lines = fIn.readlines()
	# for line in lines:
	# 	if counter % 100 == 0:
	# 		print counter
	# 	counter += 1
	# 	src, dst = line.strip('\r\n').split(',')
	# 	key = (int(src), int(dst))
	# 	if key in GLOBAL_EDGE_DICT.keys():
	# 		GLOBAL_EDGE_DICT[key] += 1
	# 	else:
	# 		GLOBAL_EDGE_DICT[key] = 1

	# fIn.close()

	# for key in GLOBAL_EDGE_DICT.keys():
	# 	fOut.write(key + '\t' + str(GLOBAL_EDGE_DICT[key]) + '\n')
	# fOut.close()

	counter = 0
	max_src = 0
	max_dst = 0
	fIn = open(input_graph_file_path, 'r')
	lines = fIn.readlines()
	for line in lines:
		if counter % 10000 == 0:
			print counter
		counter += 1

		parts = line.split('\t')
		src = parts[0]
		dst = parts[1]
		src_i = int(src)
		dst_i = int(dst)

		if src_i > max_src:
			max_src = src_i
		if dst_i > max_dst:
			max_dst = dst_i

	fIn.close()

	adj_matrix = sps.lil_matrix((max_src+1, max_dst+1), dtype=int)
	print adj_matrix.shape

	counter = 0
	fIn = open(input_graph_file_path, 'r')
	lines = fIn.readlines()
	for line in lines:
		if counter % 10000 == 0:
			print counter
		counter += 1

		parts = line.split('\t')
		src = parts[0]
		dst = parts[1]
		
		adj_matrix[int(src), int(dst)] += 1

	fIn.close()

	adj_matrix_coo = adj_matrix.tocoo()

	output_file_path = input_graph_file_path.split('.')[0] + '_wei.tsv'
	fOut = open(output_file_path, 'w')

	srcs = adj_matrix_coo.row
	dsts = adj_matrix_coo.col
	weis = adj_matrix_coo.data

	for i in range(len(srcs)):
		fOut.write(str(srcs[i]) + '\t' + str(dsts[i]) + '\t' + str(1) + '\n')


	fOut.close()

	return






if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit('usage: unwei2wei.py <input_graph_file_path>')

	input_graph_file_path = sys.argv[1]

	unwei2wei(input_graph_file_path)