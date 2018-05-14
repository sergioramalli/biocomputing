#!C:\Users\iuri\AppData\Local\Programs\Python\Python36-32\python
#!/usr/bin/env python3


"""
Program:        chromosome_CDS_15 genome browser
File:           home.py
Version:        V10
Date:           14.05.2018
Function:       contains functions needed for cgi-script
Copyright:                  Sergio Gomes Simoes
Author:                     Sergio Gomes Simoes
project_collaborators:      Sarah Griffiths, Archana Patil, Fabio Biond
Address:                    Bioinformatics, BBK, London
-------------------------------------------------------------

Description:
==============
Functions required for cgi-script 

---------------------------------------------------------------
Usage:
===========
Functions required for the cgi script 
-----------------------------------------------------------------
Revision History:
=================
V1.0   Original    													BY: Sergio Gomes

"""

import os

def getUrl(debug):

	"""
    This function grabs the current url that the user has requested 

    :param debug: boolean set to True if you want to return hardcoded url, useful if running from shell
    :return: returns list with the GET variables from the url 
    """

    #checks to see if in debug mode
	if debug:
		_GET = "get=single&type=location&term=15q22";
		_GET = "get=single&type=accession&term=AB022430";
		_GET = "get=single&type=protein-product&term=cartilage%20intermediate%20layer%20protein";
		_GET = "get=single&type=gene&term=CILP";
	else:
		#use system function to grab the full url 
		_GET = os.getenv("QUERY_STRING")

	if not _GET:
		return '';

	#splits the url and grabs all the get variables for return
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