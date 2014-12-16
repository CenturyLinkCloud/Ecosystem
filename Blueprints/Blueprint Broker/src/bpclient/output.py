# -*- coding: utf-8 -*-
"""Output formatting helper functions."""

import os
import sys
import json
import time



# TODO add sorting
def Rows(data_arr,keys,opts={}):
	max_key_len = 0
	for key in keys: 
		if len(key)>max_key_len:  max_key_len = len(key)

	table = ''
	i = 0
	for line in data_arr:
		i += 1
		table += "\n  ******************* %s. ********************\n" % (i)
		for key in keys: table += "%s:  %s\n" % (key.rjust(max_key_len+2),line[key])

	return(table)


# TSV w/o headers
def Text(data_arr,keys,opts={}):
	rows = []

	for line in data_arr:
		row = []
		for key in keys: 
			if isinstance(line[key], (basestring, int, long, float)):  row.append(str(line[key]).replace("	"," "))
			elif isinstance(line[key], (dict,)):  row.append(json.dumps(line[key]))
			else:  
				str_line = []
				for a in line[key]:  str_line.append(str(a))
				row.append(", ".join(str_line).replace(",",""))
		rows.append("	".join(row))

	return("\n".join(rows))


# TODO - Use CSV module?
def Csv(data_arr,keys,opts={'no_header': False}):
	csv = []
	if not opts['no_header']:  csv.append(",".join(keys))

	for line in data_arr:
		row = []
		for key in keys: 
			if isinstance(line[key], (basestring, int, long, float)):  row.append(str(line[key]).replace(","," "))
			else:  
				str_line = []
				for a in line[key]:  str_line.append(str(a))
				row.append(" ".join(str_line).replace(",",""))
		csv.append(",".join(row))

	return("\n".join(csv))


def Json(data_arr,keys,opts={}):
	new_data_arr = []
	for data_dict in data_arr:
		for key in data_dict.keys():
			if key not in keys:  data_dict.pop(key,None)
		new_data_arr.append(data_dict)

	if len(new_data_arr)==1:  return(new_data_arr[0])
	else:  return(new_data_arr)

