
import datetime
import socket
import sys


HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 10000        # The port used by the server



def list_str_2_list(input_str):

	parts = input_str.strip('[]').replace('u', '').replace('\'', '').split(', ')

	return ['e' + part for part in parts]


if __name__ == '__main__':


	if len(sys.argv) != 3:
		sys.exit('<usage:> <input_file_path> <output_file_path>')


	s = socket.socket()
	s.connect(('127.0.0.1', 10000))
	data = s.recv(1024)
	print data
	print 'Initialization finished.'

	input_file_path = sys.argv[1]
	output_file_path = sys.argv[2]
	
	
	

	fOut = open(output_file_path, 'w')

	counter = 0
	fIn = open(input_file_path, "r")
	lines = fIn.readlines()
	for i, line in enumerate(lines)

		# if i == end_line:#20000000:
		# 	break

		# if i < init_line:#15000000:
		# 	continue
			
		# if i % 500000 == 0:
		# 	print i

		reply_des = False
		parts = line.strip('\r\n').split('\t')

		dst_list_list = []

		if len(parts) == 3:
			src_email_id = 'e' + parts[0]
			dst_email_ids = list_str_2_list(parts[1])
			time_str = parts[2]

			dst_list_list.append(dst_email_ids)


		elif len(parts) == 4:
			src_email_id = 'e' + parts[0]
			dst_email_ids = list_str_2_list(parts[1])
			time_str = parts[2]
			cc_email_ids = list_str_2_list(parts[3])

			# dst_list = dst_email_ids + cc_email_ids
			dst_list_list.append(dst_email_ids)
			dst_list_list.append(cc_email_ids)

		else:	# this should never happen.
			sys.exit('Something went wrong.')




		s.sendall(src_email_id + '\n')
		src_personal_id = s.recv(1024).split('\n')[0]
		# print src_personal_id


		if 'could not find' not in src_personal_id:

			dst_list = dst_list_list[0]

			for dst in dst_list:

				s.sendall(dst + '\n')
				dst_personal_id = s.recv(1024).split('\n')[0]

				# if 'could not find' not in dst_personal_id:
				new_line = src_personal_id + '\t' + dst_personal_id + '\t' + time_str + '\t0\n'

				fOut.write(new_line)

			########################################

			if len(dst_list_list) == 2:

				cc_list = dst_list_list[1]

				for dst in cc_list:

					s.sendall(dst + '\n')
					dst_personal_id = s.recv(1024).split('\n')[0]

					# if 'could not find' not in dst_personal_id:
					new_line = src_personal_id + '\t' + dst_personal_id + '\t' + time_str + '\t1\n'

					fOut.write(new_line)





	s.close()

	fOut.close()

	

	# # N = 20
	# # batch_size = 3

	



