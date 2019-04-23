import json
import codecs
import os
import numpy as np
import sys
from collections import defaultdict
import matplotlib.pyplot as plt



if len(sys.argv) != 2:
	sys.exit('usage: <input_file_path>')

input_file_path = sys.argv[1]
# directory_output = 'email_to_titile_group_by_company_p/'

days_list = []
day_count_dict = {}
count_day_dict = {}

fIn = open(input_file_path, 'r')
lines = fIn.readlines()

for line in lines:

	day, count = line.strip('\r\n').split('\t')
	days_list.append(day)
	day_count_dict[day] = int(count)
	count_day_dict[int(count)] = day
fIn.close()

days_list_sorted = sorted(days_list, key=lambda d: map(int, d.split('-')))
counts_list_sorted = [day_count_dict[day] for day in days_list_sorted]

print days_list_sorted
print '-------'
print counts_list_sorted

f, axarr = plt.subplots(1, 1, figsize=(20, 6))
col = (.69, .47, .69)
title_str = 'Number of users sending emails per day'

legend_str = 'max number: ' + str(max(day_count_dict.values())) + ' date: ' + str(count_day_dict[max(day_count_dict.values())])
axarr.plot(range(len(days_list_sorted)), counts_list_sorted, color=col, label=legend_str, linestyle='--', marker='o')

day_idx_dict = dict(zip(days_list_sorted, range(len(days_list_sorted))))
print day_idx_dict

plt.xlim(left=-1, right=len(days_list_sorted))
plt.ylim(bottom=0)

plt.axvline(x=day_idx_dict['05-01'], linestyle='--', color='grey')

plt.axvline(x=day_idx_dict['06-01'], linestyle='--', color='grey')
plt.axvline(x=day_idx_dict['07-01'], linestyle='--', color='grey')


plt.xticks([day_idx_dict['05-15'], day_idx_dict['06-15'], day_idx_dict['07-15']], 
	('May', 'Jun.', 'Jul.'))

axarr.legend(loc='lower right', fontsize=10)

plt.title(title_str)
plt.tight_layout()
plt.show()