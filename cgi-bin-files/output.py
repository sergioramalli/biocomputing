#!C:\Users\iuri\AppData\Local\Programs\Python\Python36-32\python
#!/usr/bin/env python3

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
# cgitb.enable() #for debugging

debug = False;

try:

	result = False;
	message = '';
	data = {};
	_GET = getUrl(debug);
	database = DB.RetriveData();
	BLObject = BLM.middleLayerApi(database, BL);

	if 'get' not in _GET:

		raise ValueError('please provide correct url');
		
	else:

		if _GET['get'] == 'list':

			message = _GET["type"] + ' list returned';
			result = True;

			if _GET['type'] == 'genes':

				data = database.AcessGeneList();	

			elif _GET['type'] == 'accessions':

				data = database.AccessionNumberList();

			elif _GET['type'] == 'protein-products':

				data = database.ProductNameList();

			elif _GET['type'] == 'restriction-enzymes':

				data = database.AccessRestriction_Enz_List();

			elif _GET['type'] == 'locations':

				data = database.AccessChromLocList();

			else: 

				result = False;

		else:

			if 'term' not in _GET:

				raise ValueError('please provide a search term');

			result = True;
			term = urllib.parse.unquote(_GET['term'])

			if _GET['type'] == 'gene':

				data = BLObject.getAllEntryData(term, 'gene');	

			elif _GET['type'] == 'accession':

				data = BLObject.getAllEntryData(term, 'accession');	

			elif _GET['type'] == 'protein-product':

				data = BLObject.getAllEntryData(term, 'protein_product_name');	
			
			elif _GET['type'] == 'location':

				data = BLObject.getAllEntryData(term, 'chromosome_location');

			elif _GET['type'] == 'cut-site':

				sequence = 'tcgaatcgaatcgaatcgaatcgaactgccgctttdgtttcccaaaaaaaggcgctagcggatcggctagagctcttttcgcggctc'
				data = BLObject.restrictionEnzymeCutSites(sequence, 'EaeI', 1, 20);

			else: 

				result = False

		pass

except Exception as e:

	print(e)
	exit();
	result = False;
	message = str(e);

data = {
	'data' : data,
	'result' : result,
	'message' : message
}
json_string = json.dumps(data)

print(json_string)
exit()