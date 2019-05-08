#connect to our cluster
from elasticsearch import Elasticsearch



host = '10.240.0.24'
port = 9200
timeout = 1000
index = 'introduction_default'
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

def process_hits_intro(res):

	for ele in res['hits']['hits']:

		if ele['_source']['type'] == 2:

			if 'created_at' in ele['_source'] and 'referrer' in ele['_source'] and 'requester' in ele['_source'] and 'target' in ele['_source']:

				new_line = str(ele['_source']['referrer']) + '\t' + str(ele['_source']['requester']) + '\t' + str(ele['_source']['target']) + '\t' + str(ele['_source']['created_at']) + '\n'

			
			# print new_line
			fOut.write(new_line)

	return


def get_body(id_orig):
	body = {
	  "query": {
	    "multi_match" : {
	      "query": id_orig,
	      "fields": [ "target", "referrer", "requester" ] 
	    }
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

	fOut = open('Trove_depth_intro.tsv', 'w')


	fIn = open('nodes_selected.tsv', 'r')
	for line in fIn.readlines():
		id_orig, num = line.strip().split('\t')

		body = get_body(id_orig)

		res = es.search(index = index, size = batch_size, body = body, scroll = scroll_time)

		sid = res['_scroll_id']
		scroll_size = len(res['hits']['hits'])
		process_hits_intro(res)

		while scroll_size > 0:

			res_cur = es.scroll(scroll_id = sid, scroll = scroll_time)
			process_hits_intro(res_cur)

			sid = res_cur['_scroll_id']
			scroll_size = len(res_cur['hits']['hits'])
	

	fOut.close()
	# print res



