#!C:\Users\iuri\AppData\Local\Programs\Python\Python36-32\python
#!/usr/bin/env python3

"""
Program:        chromosome_CDS_15 genome browser
File:           output.py
Version:        V10
Date:           14.05.2018
Function:       A cgi-script to create a json output of the code. 
Copyright:                  Sergio Gomes Simoes
Author:                     Sergio Gomes Simoes
project_collaborators:      Sarah Griffiths, Archana Patil, Fabio Biond
Address:                    Bioinformatics, BBK, London
-------------------------------------------------------------

Description:
==============
Depending on the url the requests output different information as a jsonObject. 
The general format is {data: 'the data being requested', 'message' : 'a message from the server usually a error message', 
'result' : boolean depending if request was successful or errored
}

Example Requests 
http://student.cryst.bbk.ac.uk/cgi-bin/cgiwrap/~gs001/output.py/?get=list&type=locations
get=single&type=location&term=15q22
get=single&type=accession&term=AB022430
get=single&type=protein-product&term=cartilage%20intermediate%20layer%20protein
get=single&type=gene&term=CILP

This procedural block code interactions with both the middle and the top layers 

---------------------------------------------------------------
Usage:
===========
To browser files as per requirement of coursework
-----------------------------------------------------------------
Revision History:
=================
V1.0  Original    													BY: Sergio Gomes

"""

import cgi,cgitb, os
import json
import urllib.parse
import sys
from lib import archana as DB
from lib import businessLogicMainFile as BLM
from lib import businessLogic as BL

from home import getUrl

print("Content-Type: application/json")  
print()             
print()               

## Uncomment cgitb to enable browser debugging, and set debug true to run code as shell 
# cgitb.enable() #for debugging
debug = False;

try:

	##The block sets up connections to db and set variables for the jsonObjects
	result = False;
	message = '';
	data = {};

	##db connection and middle layer 
	database = DB.RetriveData();
	BLObject = BLM.middleLayerApi(database, BL);

	##This function grabs the url, set debug to true to run in shell 
	_GET = getUrl(debug);

	if 'get' not in _GET:

		raise ValueError('please provide correct url');
		
	else:

		# if this condition is true then you are requesting a list i.e genes, accession codes etc... 
		if _GET['get'] == 'list':

			message = _GET["type"] + ' list returned';
			result = True;

			if _GET['type'] == 'genes':

				#grab a list of genes 
				data = database.AccessGeneList();

			elif _GET['type'] == 'sequences':

				#grab a list of genes plus more information include sequences 
				data = database.AccessGeneList('sequences');	

			elif _GET['type'] == 'accessions':

				#grabs a list of accession numbers 
				data = database.AccessionNumberList();

			elif _GET['type'] == 'protein-products':

				#grabs a list of products names 
				data = database.ProductNameList();

			elif _GET['type'] == 'restriction-enzymes':

				#grabs a list of restriction enzymes 
				data = database.AccessRestriction_Enz_List();

			elif _GET['type'] == 'locations':

				#grabs a list of chromosomal loctions 
				data = database.AccessChromLocList();

			else: 

				result = False;

		else:

			# if for example you want to grab a single item 
			if 'term' not in _GET:

				raise ValueError('please provide a search term');

			result = True;
			#cleans string from url
			term = urllib.parse.unquote(_GET['term'])

			if _GET['type'] == 'gene':

				#grabs single gene entry from a gene term. Includes middle analysis 
				data = BLObject.getAllEntryData(term, 'gene');	

			elif _GET['type'] == 'accession':

				#grabs single gene entry from a accession term. Includes middle analysis 
				data = BLObject.getAllEntryData(term, 'accession');	

			elif _GET['type'] == 'protein-product':

				#grabs single gene entry from a product term. Includes middle analysis 
				data = BLObject.getAllEntryData(term, 'protein_product_name');	
			
			elif _GET['type'] == 'location':

				#grabs single gene entry from a location term. Includes middle analysis 
				data = BLObject.getAllEntryData(term, 'chromosome_location');

			elif _GET['type'] == 'cut-site':

				#This was meant to provide cut-site information but wasnt completed 
				sequence = 'tcgaatcgaatcgaatcgaatcgaactgccgctttdgtttcccaaaaaaaggcgctagcggatcggctagagctcttttcgcggctc'
				data = BLObject.restrictionEnzymeCutSites(sequence, 'EaeI', 1, 20);

			else: 

				result = False

		pass

except Exception as e:

	#If there is an error then, then the result is set to false,
	#this way someone accessing the json from the api can deal with the empty result 
	result = False;
	message = str(e);

#Creates the json object and outputs it to the browser 
data = {
	'data' : data,
	'result' : result,
	'message' : message
}
json_string = json.dumps(data)
print(json_string)
exit()