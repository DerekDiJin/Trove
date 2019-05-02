import os
import sys
import datetime
import collections
import networkx as nx
import csv
import json
import scipy.sparse as sps
import numpy as np
from scipy import stats
from scipy.stats import norm,rayleigh
import matplotlib.pyplot as plt

def plot_seq(axarr, marker, deg, cnt, type, title):

	n = axarr[marker].hist(deg, normed=True, bins=cnt, alpha=0.33, label=title)	
	# axarr[marker].set_title(type + " Degree distribution for " + str(title))
	counts = n[0]
	bv = n[1]
	# print(n[0])
	# print(bins)
	x = np.linspace(min(bv), max(bv),100)
	print(deg)
	print(bv, counts)
	param = stats.lognorm.fit(deg,floc=0)
	pdf_fitted = stats.lognorm.pdf(x,param[0], loc=param[1], scale=param[2])
	axarr[marker].plot(x, pdf_fitted, label=title)
	axarr[marker].set_ylabel("Frequency")
	axarr[marker].set_xlabel(type + " Degree")
		
	return



def graph_analyze(input_graph_file):
	
	delimiter = '\t'
	
	raw = np.genfromtxt(input_graph_file, dtype=int)
	rows = raw[:,0]
	cols = raw[:,1]
	weis = raw[:,2]

	check_eq = True
	max_id = int(max(max(rows), max(cols)))
	num_nodes = max_id + 1

	if max(rows) != max(cols):
		rows = np.append(rows,max(max(rows), max(cols)))
		cols = np.append(cols,max(max(rows), max(cols)))
		weis = np.append(weis, 0)
		check_eq = False

	adj_matrix = sps.lil_matrix( sps.csc_matrix((weis, (rows, cols))))

	keys = np.arange(num_nodes)
	values_out = np.asarray(adj_matrix.sum(1).T)[0]
	values_in = np.asarray(adj_matrix.sum(0))[0]

	dict_outdeg = dict( zip(keys, values_out) )
	dict_indeg = dict( zip(keys, values_in) )




	print('Number of nodes: ' + str(num_nodes))
	print('Number of edges: ' + str(raw.shape[0]))# sum(weis)))

	print('Max in_degree ' + str(max(values_in)))
	print('Max out_degree ' + str(max(values_out)))

	print('Medain in_degree ' + str(np.median(values_in)))
	print('Medain out_degree ' + str(np.median(values_out)))

	
	

	
	return
	
	


if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit('usage: title_parameters.py <input_graph_file>')

	input_graph_file = sys.argv[1]

	graph_analyze(input_graph_file)



