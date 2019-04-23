
import datetime
import socket
import sys


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 10000        # The port used by the server



def list_str_2_list(input_str):

	parts = input_str.strip('[]').replace('u', '').replace('\'', '').split(', ')

	return [part for part in parts]

def construct_map(input_lookup_file_path):

	result = {}

	fIn = open(input_lookup_file_path, 'r')
	lines = fIn.readlines()

	for line in lines:
		old_id, new_id = line.strip('\r\n').split('\t')
		result[old_id] = new_id

	fIn.close()

	return result


if __name__ == '__main__':


	if len(sys.argv) != 4:
		sys.exit('<usage:> <input_intro_file_path> <input_lookup_file_path> <output_file_path>')


	input_intro_file_path = sys.argv[1]
	input_lookup_file_path = sys.argv[2]
	output_file_path = sys.argv[3]

	old_new_id_map = construct_map(input_lookup_file_path)

	fOut = open(output_file_path, 'w')

	fIn = open(input_intro_file_path, 'r')
	lines = fIn.readlines()

	for line in lines:

		id_0, id_1, id_2, time_str = line.strip('\r\n').split('\t')

		if (id_0 in old_new_id_map) and (id_1 in old_new_id_map) and (id_2 in old_new_id_map): 

			id_0_new = old_new_id_map[id_0]
			id_1_new = old_new_id_map[id_1]
			id_2_new = old_new_id_map[id_2]

			new_line = id_0_new + '\t' + id_1_new + '\t' + id_2_new + '\t' + time_str + '\n'

			fOut.write(new_line)

	fIn.close()
	fOut.close()






