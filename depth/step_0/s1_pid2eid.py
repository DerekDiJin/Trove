
import datetime
import socket
import sys


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 10000        # The port used by the server



def list_str_2_list(input_str):

	parts = input_str.strip('[]').replace('u', '').replace('\'', '').split(', ')

	return [part for part in parts]


if __name__ == '__main__':


	if len(sys.argv) != 3:
		sys.exit('<usage:> <input_pid_selected_file_path> <output_mapping_file_path>')


	s = socket.socket()
	s.connect(('127.0.0.1', 10000))
	data = s.recv(1024)
	print data
	print 'Initialization finished.'

	input_pid_selected_file_path = sys.argv[1]
	output_mapping_file_path = sys.argv[2]

	fOut = open(output_mapping_file_path, 'w')

	counter = 0
	fIn = open(input_pid_selected_file_path, 'r')
	lines = fIn.readlines()
	for i, line in enumerate(lines):

		if i == 1800000:
			break

		if i < 1600000:
			continue
			
		if i % 10000 == 0:
			print i

		pid, counts = line.strip('\r\n').split('\t')
		query = 'p' + pid
		# print query


		s.sendall(query + '\n')
		eids = s.recv(1024).split('\n')[0]
		# print eids
		
		new_line = pid + '\t' + eids + '\n'

		fOut.write(new_line)




	s.close()

	fIn.close()
	fOut.close()

	

	# # N = 20
	# # batch_size = 3

	



