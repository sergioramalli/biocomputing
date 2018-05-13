#!C:\Users\iuri\AppData\Local\Programs\Python\Python36-32\python
#!/usr/bin/env python3

import cgi,cgitb, os
import json
import urllib.parse
import sys
from lib import archana as DB
from lib import businessLogicMainFile as BL
from lib import businessLogic

from home import getUrl

print("Content-Type: application/json")  
print()             
print()               
cgitb.enable() #for debugging

debug = True;

try:

	result = False;
	message = '';
	data = {};
	_GET = getUrl(debug);
	database = DB.RetriveData();
	BLObject = BL.middleLayerApi(database);

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

			elif _GET['type'] == 'protein-product':

				data = database.ProductNameList();

			elif _GET['type'] == 'enzymes':

				data = database.AccessRestriction_enzymeList();

			else:

				data = x.AccessChromLocList();

		else:

			if _GET['type'] == 'gene':

				data = BLObject.getAllEntryData(_GET['term'], 'gene');	

			elif _GET['type'] == 'accession':

				data = BLObject.getAllEntryData(_GET['term'], 'accession');	

			elif _GET['type'] == 'protein-product':

				term = urllib.parse.unquote(_GET['term'])
				data = BLObject.getAllEntryData(term, 'protein_product_name');	
			
			else:

				data = BLObject.getAllEntryData(_GET['term'], 'chromosome_location');

		pass

except Exception as e:

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


x = getAllGenes();

xx = getAllEntryData(x[0], 'gene');
# print(xx);

xx = getAllEntryData('cartilage intermediate layer protein', 'protein_product_name');
# print(xx);

xx = getAllEntryData('15q22', 'chromosome_location');
# print(xx);

xx = getAllEntryData('AB022430', 'accession');
# print(xx)