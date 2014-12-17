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
def Text(data,keys,opts={}):
	for key in keys: 
		if isinstance(data[key], (basestring, int, long, float)):  row = str(data[key]).replace("	"," ")
		elif isinstance(data[key], (dict,)):  row = json.dumps(data[key])
		else:  
			str_line = []
			for a in data[key]:  str_line.append(str(a))
			row = ", ".join(str_line).replace(",","")

	return(row)


# TODO - Use CSV module?
def Csv(data,keys,opts={'no_header': False}):
	if not opts['no_header']:  csv.append(",".join(keys))

	for key in keys: 
		if isinstance(data[key], (basestring, int, long, float)):  csv = str(data[key]).replace(","," ")
		else:  
			str_data = []
			for a in data[key]:  str_data.append(str(a))
			csv =" ".join(str_data).replace(",","")

	return(csv)


def Json(data,keys,opts={}):
	for key in data.keys():
		if key not in keys:  data.pop(key,None)

	return(data)

