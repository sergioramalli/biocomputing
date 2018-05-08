#!C:\Users\iuri\AppData\Local\Programs\Python\Python36-32\python
#!/usr/bin/env python3

import cgi
from lib import business_layer

print("Content-Type: text/html")    
print()                             
 
import cgi,cgitb
import os
# cgitb.enable() #for debugging

# the query string, which contains the raw GET data
# (For example, for http://example.com/myscript.py?a=b&c=d&e
# this is "a=b&c=d&e")
_GET = os.getenv("QUERY_STRING")
_GET = "get=list&type=gene";

arr = {};
_GET = _GET.split('&')
for x in _GET:

	x = x.split('=');
	arr[x[0]] = x[1];
	pass

_GET = arr;

if not _GET:

	raise ValueError('no get variables provided')

if 'get' not in _GET:

	raise ValueError('please provide correct url');
	
else:

	if _GET['get'] == 'list':

		if _GET['type'] == 'genes':

			print('get list of genes');

		elif _GET['type'] == 'accessions':

			print('get list of accessions');

		elif _GET['type'] == 'protein_product':

			print('protein products');

		elif _GET['type'] == 'locations':

			print('locations');

		elif _GET['type'] == 'enzymes':

			print('enzymes');

		else:

			print('chromloclist');

	else:

		if _GET['type'] == 'accessions':
			print('get single');

	pass
