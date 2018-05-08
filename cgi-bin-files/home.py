#!C:\Users\iuri\AppData\Local\Programs\Python\Python36-32\python
#!/usr/bin/env python3

import os

def getUrl():

	# the query string, which contains the raw GET data
	# (For example, for http://example.com/myscript.py?a=b&c=d&e
	# this is "a=b&c=d&e")
	_GET = os.getenv("QUERY_STRING")
	# _GET = "get=list&type=gene";

	if not _GET:
		return '';


	arr = {};
	_GET = _GET.split('&')
	for x in _GET:

		x = x.split('=');
		arr[x[0]] = x[1];
		pass

	_GET = arr;

	if not _GET:

		raise ValueError('no get variables provided')
	pass
	
	return _GET;