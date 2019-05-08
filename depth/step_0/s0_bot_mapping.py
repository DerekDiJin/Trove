#connect to our cluster
from elasticsearch import Elasticsearch



host = '10.240.0.24'
port = 9200
timeout = 1000
index = 'v2_user_profile_default'
batch_size = 1000

scroll_time = '2m'


def process_hits(res):

	for ele in res['hits']['hits']:

		if 'header_from' in ele['_source']['data'] and 'header_to' in ele['_source']['data']:

			if 'header_cc' in ele['_source']['data']:

				new_line = str(ele['_source']['data']['header_from']) + '\t' + str(ele['_source']['data']['header_to']) + '\t' + str(ele['_source']['data']['message_time']) + '\t' + str(ele['_source']['data']['header_cc']) + '\n'

			else:

				new_line = str(ele['_source']['data']['header_from']) + '\t' + str(ele['_source']['data']['header_to']) + '\t' + str(ele['_source']['data']['message_time']) + '\n'

			fOut.write(new_line)

	return

def process_hits_bot_mapping(res, fOut):

	for ele in res['hits']['hits']:


		if 'person_id' in ele['_source'] and 'is_bot' in ele['_source']:

			try:
			# new_line = str(ele['_source']['referrer']) + '\t' + str(ele['_source']['requester']) + '\t' + str(ele['_source']['target']) + '\t' + str(ele['_source']['created_at']) + '\n'
				# new_line = str(ele['_source']['person_id']) + '\t' + str(ele['_source']['is_bot']) + '\t' + \
				# 		   str(ele['_source']['profile']['history']['first_communication']['date']) + '\t' + str(ele['_source']['profile']['history']['last_communication']['date']) + '\n'
				new_line = str(ele['_source']['person_id']) + '\t' + str(ele['_source']['is_bot']) + '\n'

		# print new_line
				fOut.write(new_line)
			except:
				print('fields missing')

	return


def get_body():
	body = {
		"query": {
        	"match_all": {}
    	}
	}
	return body


if __name__ == '__main__':

	es = Elasticsearch(
		[
			{
				'host': host, 
				'port': port
			}
		],
		timeout=timeout
	)
	

	# N = 20
	# batch_size = 3

	fOut = open('Trove_depth_bot_mapping_complete.tsv', 'w')


	body = get_body()

	res = es.search(index = index, size = batch_size, body = body, scroll = scroll_time)
	# print res

	sid = res['_scroll_id']
	scroll_size = len(res['hits']['hits'])
	process_hits_bot_mapping(res, fOut)

	while scroll_size > 0:

		res_cur = es.scroll(scroll_id = sid, scroll = scroll_time)
		process_hits_bot_mapping(res_cur, fOut)

		sid = res_cur['_scroll_id']
		scroll_size = len(res_cur['hits']['hits'])
	


	fOut.close()
	# print res



