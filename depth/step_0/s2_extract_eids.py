#connect to our cluster
from elasticsearch import Elasticsearch
import sys


host = '10.240.0.37'
port = 9200
timeout = 1000
index = 'mail_default'
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
              "gte": "2018-07-01T00:00:00+00:00",
              "lte": "2018-12-01T00:00:00+00:00"
            }
          }
        }
      ]
    }
  }
}
scroll_time = '2m'


def process_hits(res, fOut):

	for ele in res['hits']['hits']:

		if 'from' in ele['_source']['header'] and 'to' in ele['_source']['header']:

			if 'cc' in ele['_source']['header']:
				new_line = str(ele['_source']['header']['from']) + '\t' + str(ele['_source']['header']['to']) + '\t' + str(ele['_source']['header']['message_time']) + '\t' + str(ele['_source']['header']['cc']) + '\n'
			else:
				new_line = str(ele['_source']['header']['from']) + '\t' + str(ele['_source']['header']['to']) + '\t' + str(ele['_source']['header']['message_time']) + '\n'

			fOut.write(new_line)

	return

def get_body(id_orig):
	body = {
	  "query": {
	    "multi_match" : {
	      "query": id_orig,
	      "fields": [ "header.from", "header.to", "header.cc" ]
	    }
	  }
	}
	return body


if __name__ == '__main__':
	

	if len(sys.argv) != 3:
		sys.exit('usage: <input_eid_file_path> <output_file_path>')

	input_eid_file_path = sys.argv[1]
	output_file_path = sys.argv[2]


	eid_selected = set([])
	fIn = open(input_eid_file_path, 'r')
	for line in fIn.readlines():
		if 'could not' in line:
			continue
		pid, eids = line.strip().split('\t')

		for eid in eids.split(','):
			eid_selected.add(eid)
	fIn.close()

	es = Elasticsearch(
		[
			{
				'host': host, 
				'port': port
			}
		],
		timeout=timeout
	)


	fOut = open(output_file_path, 'w')


	# body_str = '{"from": ' + str(i*batch_size) + ',"size": ' + str(batch_size) + ', "query": {"bool": {"filter": [{"range": {"data.message_time": {"gte": "2018-02-01T00:00:00+00:00","lte": "2018-05-01T00:00:00+00:00"}}}]}}}'

	for eid in eid_selected:

		body = get_body(eid)

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



