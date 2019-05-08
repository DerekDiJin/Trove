#connect to our cluster
from elasticsearch import Elasticsearch



host = '10.240.0.37'
port = 9200
timeout = 1000
index = 'message_store_default'
batch_size = 1000
body = {
  "query": {
    "bool": {
      "must_not" : {
        "term":  { "data.is_mailing_list": True }
      },
      "filter": [
        {
          "range": {
            "data.message_time": {
              "gte": "2018-05-01T00:00:00+00:00",
              "lte": "2018-08-01T00:00:00+00:00"
            }
          }
        }
      ]
    }
  }
}
scroll_time = '2m'


def process_hits(res):

	for ele in res['hits']['hits']:

		if 'header_from' in ele['_source']['data'] and 'header_to' in ele['_source']['data']:

			if 'header_cc' in ele['_source']['data']:
				new_line = str(ele['_source']['data']['header_from']) + '\t' + str(ele['_source']['data']['header_to']) + '\t' + str(ele['_source']['data']['message_time']) + '\t' + str(ele['_source']['data']['header_cc'])
			else:
				new_line = str(ele['_source']['data']['header_from']) + '\t' + str(ele['_source']['data']['header_to']) + '\t' + str(ele['_source']['data']['message_time'])

			if 'is_reply_desired' in ele['_source']['data']:
				new_line += '\t' + str(ele['_source']['data']['is_reply_desired']) + '\n'
				print 'Extra field'
				print new_line
			else:
				new_line += '\n'
				print 'Normal'
				print new_line

			# fOut.write(new_line)

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

	fOut = open('Trove_10M.tsv', 'w')


	# body_str = '{"from": ' + str(i*batch_size) + ',"size": ' + str(batch_size) + ', "query": {"bool": {"filter": [{"range": {"data.message_time": {"gte": "2018-02-01T00:00:00+00:00","lte": "2018-05-01T00:00:00+00:00"}}}]}}}'

	res = es.search(index = index, size = batch_size, body = body)#, scroll = scroll_time)

	# sid = res['_scroll_id']
	# scroll_size = len(res['hits']['hits'])
	process_hits(res)

	# while scroll_size > 0:

	# 	res_cur = es.scroll(scroll_id = sid, scroll = scroll_time)
	# 	process_hits(res_cur)

	# 	sid = res_cur['_scroll_id']
	# 	scroll_size = len(res_cur['hits']['hits'])
	

	# fOut.close()
	# print res



