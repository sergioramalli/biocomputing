#!C:\Users\iuri\AppData\Local\Programs\Python\Python36-32\python
#!/usr/bin/env python3

import cgi,cgitb, os
import json
from lib import businessLogic as BL
from lib import db_access 
from home import getUrl

print("Content-Type: application/json")  
print()          
print()                   
cgitb.enable() #for debugging

try:

	x = db_access.RetriveData()
	_GET = getUrl();
	result = False;
	message = '';
	data = {};

	if 'get' not in _GET:

		raise ValueError('please provide correct url');
		
	else:

		if _GET['get'] == 'list':

			message = _GET["type"] + ' list returned';
			result = True;

			if _GET['type'] == 'genes':

				data = x.AcessGeneList();	

			elif _GET['type'] == 'accessions':

				data = x.AccessionNumberList();

			elif _GET['type'] == 'protein-product':

				data = x.ProductNameList();

			elif _GET['type'] == 'enzymes':

				data = x.AccessRestriction_enzymeList();

			else:

				data = x.AccessChromLocList();

		else:

			#dummy data
			with open ('lib/seq.txt','r') as f:
			    sequence = f.read().split()

			# start = 3360
			# end = 4300

			# parsedSequence = BL.ParseSequence(sequence)
			# codingRegion = BL.codingRegion(start,end,parsedSequence)
			# mrnaSequence = BL.translate(codingRegion)
			# splitSequence = BL.CodonSequence(mrnaSequence)
			# translatedAndAligned = BL.alignseq(splitSequence)
			# justAminoAcids = BL.translatedSequence(splitSequence)#check this
			# codonFrequency = BL.codonFreq(splitSequence)# need to edit to incorporate total frequencies
			# restrictionEnzymeCutSites = BL.restrictionEnzyme('ttgtc', start, end, parsedSequence) #returned as dictionary

			if _GET['type'] == 'accessions':
				print('get single');

		pass

except Exception as e:

	result = False;
	message = e;

data = {
	'data' : data,
	'result' : result,
	'message' : message
}
json_string = json.dumps(data)

print(json_string)
exit()