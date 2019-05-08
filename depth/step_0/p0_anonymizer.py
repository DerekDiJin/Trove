
import datetime
import socket
import sys



def write_mapping(OLD_NEW_DICT, input_file_path):

	output_file_path = input_file_path.split('/')[-1].split('.')[-2] + '_lookup.tsv'
	fOut = open(output_file_path, 'w')

	for old_id in OLD_NEW_DICT:
		newline = old_id + '\t' + str(OLD_NEW_DICT[old_id]) + '\n'
		fOut.write(newline)

	fOut.close()

	return



if __name__ == '__main__':


	if len(sys.argv) != 2:
		sys.exit('<usage:> <input_file_path>')


	UNIQUE_ID_SET = set([])
	OLD_NEW_DICT = {}

	input_file_path = sys.argv[1]
	fIn = open(input_file_path, 'r')
	for line in fIn.readlines():
		src, dst, wei = line.strip('\r\n').split('\t')

		UNIQUE_ID_SET.add(src)
		UNIQUE_ID_SET.add(dst)


	fIn.close()


	OLD_NEW_DICT = dict( zip(list(UNIQUE_ID_SET), range(len(UNIQUE_ID_SET))) )


	write_mapping(OLD_NEW_DICT, input_file_path)

	############################

	output_file_path = input_file_path.split('/')[-1].split('.')[-2] + '_anonymized.tsv'
	fOut = open(output_file_path, 'w')

	fIn = open(input_file_path, 'r')
	for line in fIn.readlines():
		src, dst, wei = line.strip('\r\n').split('\t')
		newline = str(OLD_NEW_DICT[src]) + '\t' + str(OLD_NEW_DICT[dst]) + '\t' + wei + '\n'
		fOut.write(newline)

	fIn.close()
	fOut.close()
		






