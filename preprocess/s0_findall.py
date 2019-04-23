#connect to our cluster
from elasticsearch import Elasticsearch



host = '10.240.0.24'
port = 9200
timeout = 1000
index = 'v2_user_relationship_default'
batch_size = 1000
body = {
  # "query": {
  #   "bool": {
  #     "filter": [
  #       {
  #         "range": {
  #           "stats.raw_score_out": {
  #             "gte": 100
  #           }
  #         }
  #       }
  #     ]
  #   }
  # }
}
scroll_time = '2m'


def process_hits(res, fOut):

	for ele in res['hits']['hits']:

		if 'from_person_id' in ele['_source'] and 'to_person_id' in ele['_source'] and 'stats' in ele['_source']:

			if 'total_emails_in' in ele['_source']['stats'] and 'total_emails_out' in ele['_source']['stats']:
				new_line_1 = str(ele['_source']['from_person_id']) + '\t' + str(ele['_source']['to_person_id']) + '\t' + str(ele['_source']['stats']['total_emails_out']) + '\n'
				new_line_2 = str(ele['_source']['to_person_id']) + '\t' + str(ele['_source']['from_person_id']) + '\t' + str(ele['_source']['stats']['total_emails_in']) + '\n'
				fOut.write(new_line_1)
				fOut.write(new_line_2)
			else:
				continue

	return


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

	fOut = open('Trove_ALL_edgelist.tsv', 'w')


	# body_str = '{"from": ' + str(i*batch_size) + ',"size": ' + str(batch_size) + ', "query": {"bool": {"filter": [{"range": {"data.message_time": {"gte": "2018-02-01T00:00:00+00:00","lte": "2018-05-01T00:00:00+00:00"}}}]}}}'

	res = es.search(index = index, size = batch_size, body = body, scroll = scroll_time)

	sid = res['_scroll_id']
	scroll_size = len(res['hits']['hits'])
	process_hits(res, fOut)

	while scroll_size > 0:

		res_cur = es.scroll(scroll_id = sid, scroll = scroll_time)
		process_hits(res_cur, fOut)

		sid = res_cur['_scroll_id']
		scroll_size = len(res_cur['hits']['hits'])
	

	fOut.close()
	# print res



