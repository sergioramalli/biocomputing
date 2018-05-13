#!/usr/bin/env python3

"""
Program:        chromosome_CDS_15 genome browser
File:           DB_layer.py
Version:        V4.1
Date:           07.05.2018
Function:       fetches the requested data from Chrom CDS 15 DB, returns it to the middle/from end layer either as a list or dictionary form
Copyright:                  Archana Patil
Author:                     Archana Patil
project_collaborators:      Sarah Griffiths, Sergio Ramalli, Fabio Biond
Address:                    Bioinformatics, BBK, London
-------------------------------------------------------------

Description:
==============
This programme provides a 'data access tier' - Python wrappers to the SQL that return the data required by the middle tier - an abstraction of the database design that returns the data requested
---------------------------------------------------------------
Usage:
===========
ChromosomeCDS15_genome_browser
-----------------------------------------------------------------
Revision History:
=================
V1.0 21.03.2018     Original    													BY: Archana Patil
V2.0 09.04.2018     Re-Work     													BY: Archana Patil
V3.0 06.05.2018     Final copy  													BY: Archana Patil
V3.1 07.05.2018     fixed issues during integration  								BY: Archana Patil
V4.0 08.05.2018		amendments of functions requested by middle and front layer     BY: Archana Patil
V4.1 09.05.2018		teseting on local db											BY: Archana Patil
"""

import pymysql.cursors

class DatabaseAccess(object):
	"""
	This class contains functions for DB connection set up, creating cursors and executing SQL script

	"""

	def DB_connection (self):
		"""
		This function establishes connection with database which holds the reuqired data from chrom_CDS_ 15 file
		:param: a config file containg connection properties
		:output: a successful connection to database
		
		"""
		try:
				#open a database connection
				from config import connection_properties
				db_connection = pymysql.connect(**connection_properties, use_unicode=True, charset="utf8")
			   
		except Exception as e:
				#expections happens when an error is raised/thrown. Those errors would be caught here
				#if exception is made close connection here 
				print('There was an issue: ', e)
				exit();

		
		return (db_connection)
					
			
	def DB_EndConnection (self, db_connection):

		"""
		This function will close DB connection
		:param: a db_connection cursor
		output:closing the connection

		"""
		try:
				db_connection.close()
				
		except Exception as e:
				#expections happens when an error is raised/thrown. Those errors would be caught here
				#if exception is made close connection here 
				print('There was an issue: ', e)
				exit();

		return ()

	def Prepare_Cursor(self, db_connection):

		"""
		This fuction creats a database cursor to run the sql querries and to set the data encoding to SET utf8
		:param: input nothing
		output: a cursor

		"""
		try:
				# prepare a cursor object using cursor() method
				
				cursor = db_connection.cursor(pymysql.cursors.DictCursor)
		
				cursor.execute('SET NAMES utf8;')
				cursor.execute('SET CHARACTER SET utf8;')
				cursor.execute('SET character_set_connection=utf8;')

		except Exception as e:
				#expections happens when an error is raised/thrown. Those errors would be caught here
				#if exception is made close connection here 
				print('There was an issue: ', e)
				exit();
				
		return(cursor)

	def Script_Execute (self, sql_query):
			
		"""

		This function will execute a sql querry 
		input = sql query
		output = cursor
		
		"""
		try:

				connect = self.DB_connection()
				cursor = self.Prepare_Cursor(connect) 
		# Create SQL statement to find list of the gene from Table Gene
				sql = sql_query 
	  
				cursor.execute(sql)
				result = cursor.fetchall()
				cursor.close()
				self.DB_EndConnection(cursor) #closing connection

		except Exception as e:
				#expections happens when an error is raised/thrown. Those errors would be caught here
				#if exception is made close connection here 
				print('There was an issue: ', e)
				exit();
		
		return result #returning result as dictionary

	   
class RetriveData(object):
	"""
	This class extracts the querried data from the database 

	"""

	def AcessGeneList (self):
			
		"""

		This function will return a summary list of the gene identifier (gene name)
		input = sql
		output = a list containing all the  gene identifier (gene_name)
		
		"""
		gene_list = []
		
		# Create SQL statement to find list of the gene from Table Gene
		sql = "SELECT gene_name From   Gene" 
	  	
		db = DatabaseAccess();
		result = db.Script_Execute(sql);
		gene_list = [item['gene_name'] for item in result]
					 
		return(gene_list) #returning result as dictionary

			
	def AccessChromLocList (self):
			
		"""

		This function will return a summary list of the Chromosome locations of all the genes
		input = sql
		output = a list containing chromosome location of all the genes
		
		"""
		Chrom_Loc_list = []

		# Create SQL statement to find list of chromosome locations of all the genes from Table Gene    
		sql = "SELECT chromosome_loc From   Gene"

		db = DatabaseAccess();
		result = db.Script_Execute(sql);
		Chrom_Loc_list = [item['chromosome_loc'] for item in result]
					 
		return(Chrom_Loc_list)

	
	def AccessionNumberList (self):
			
		"""

		This function will return a summary list of the accession number
		input = gene_name (exact or partial name ?), and cursor
		output = a list containing a list of all the accession numbers
		
		"""
		accessionNo_list = []
		
		# Create SQL statement to find list of the gene from Table Gene
		sql = "SELECT accession_number From   Gene"

		db = DatabaseAccess();
		result = db.Script_Execute(sql);
		accessionNo_list = [item['accession_number'] for item in result]
					 
		return(accessionNo_list)      

	
	def ProductNameList (self):
			
		"""

		This function will return a summary list of the protein product names
		input = gene_name (exact or partial name ?), and sql
		output = a list containing a list of all protein product names
		
		"""
		ProteinProductName_list = []

		# Create SQL statement to find list of the gene from Table Gene
		sql = "SELECT product_name From Protein"

		db = DatabaseAccess();
		result = db.Script_Execute(sql);
		ProteinProductName_list = [item['product_name'] for item in result]
					 
		return(ProteinProductName_list)      


	
	def AccessGeneData (self, gene_name):
			
		"""

		This function will search DB based on gene name and returns a dict containing gene identifier, accession number, Chromosome location and protein product name
		input = gene_name (exact or partial name ?), and sql
		output = accession number, gene identifier, chromosome location, protein product name for a queried gene identifier
		
		"""
		
		# Create SQL statement to find list of the gene from Table Gene
		sql = "Select g.gene_name, g.accession_number, g.chromosome_loc, p.product_name From   Gene g, Sequence s, Protein p Where g.gene_id = s.gene_id AND  s.sequence_id  = p.sequence_id AND upper(g.gene_name) LIKE ('%" + gene_name + "%');" 
	  
		db = DatabaseAccess();
		result = db.Script_Execute(sql);             
		
		return result #returning result as dictionary


	def AccessAccession_number (self, accession_number):
			
		"""

		This function will search the db based on accession number and will return a dictionary cantaining the gene identifier, Chromosome location and protein product name for the qureied accession number
		input = accession_number, and sql
		output = accession number, gene name, chromosome location, protein product name for a queried accession number 
		
		"""
		
		# Create SQL statement to find list of the gene from Table Gene
		sql = "Select g.gene_name, g.accession_number, g.chromosome_loc, p.product_name From   Gene g, Sequence s, Protein p Where g.gene_id = s.gene_id AND  s.sequence_id  = p.sequence_id AND g.accession_number = '" + accession_number + "';" 
	  
		db = DatabaseAccess();
		result = db.Script_Execute(sql);             
		
		return result #returning result as dictionary

	def AccessChromosome_loc (self, chromosome_loc):
			
		"""

		This function will search the db based on chromosome_loc and will return a dictionary cantaining the gene identifier, accession number and protein product name for the qureied chromosome location
		input = chromosome location, and sql
		output = accession number, gene name, protein product name for queried chromosome loctation 
		
		"""
		
		# Create SQL statement to find list of the gene from Table Gene
		sql = "Select g.gene_name, g.accession_number, g.chromosome_loc, p.product_name From   Gene g, Sequence s, Protein p Where g.gene_id = s.gene_id AND  s.sequence_id  = p.sequence_id AND g.chromosome_loc LIKE '" + chromosome_loc + "';" 
	  
		db = DatabaseAccess();
		result = db.Script_Execute(sql);             
		
		return result #returning result as dictionary

	def AccessProduct_name (self, product_name):
			
		"""

		This function will search the db based on product name and will return a dictionary cantaining the gene identifier, Chromosome location, asseccsion number and protein product name for the qureied product name
		input = accession_number, and sql
		output = accession number, gene name, chromosome location, protein product name for a queried product name 
		
		"""
		
		# Create SQL statement to find list of the gene from Table Gene
		sql = "Select g.gene_name, g.accession_number, g.chromosome_loc, p.product_name From   Gene g, Sequence s, Protein p Where g.gene_id = s.gene_id AND  s.sequence_id  = p.sequence_id AND upper(p.product_name) LIKE upper('%" + product_name + "%');" 
	  
		db = DatabaseAccess();
		result = db.Script_Execute(sql);             
		
		return result #returning result as dictionary

	def AccessSeqData_AccNo (self, accession_number):
			
		"""

		This function will search the db for sequence information based on accession number and will return a dict containing gene name, gene length,  gDNA sequence, CDS_join, codon start position and translation seq
		which will be used by middle layer to derive CDS, cal codon usage etc
		input = accession number, sql
		output = a dictionary containing gene_name, length of the gene, gDNA sequence (nucleotide seq), CDS_join, codon start position and translation seq for the querried gene
		
		"""
		
		# Create SQL statement to find a nucleotide seq, cds start and end postion, cds from Tables Gene and Sequence
		sql = "Select   g.gene_name, g.length, s.gDNA, s.CDS_join, s.codon_start, s.translation From Gene g, Sequence s Where g.gene_id = s.gene_id AND g.accession_number = '" + accession_number + "';" 
		db = DatabaseAccess()
		result = db.Script_Execute(sql)
		return result #returning result as dictionary


	

	def AccessSequenceSummary (self):
			
		"""

		This function will return a  summary of all the gene name, length,  gDNA sequence, CDS_join, codon start position and translation seq
		which will be used by middle layer to derive CDS, cal codon usage etc
		input = sql
		output = a dictionary containing gene name length of the gene, gDNA sequence (nucleotide seq), CDS_join, codon start position and translation seq
		
		"""

		# Create SQL statement to find a nucleotide seq, cds start and end postion, cds from Tables Gene and Sequence
		sql = "Select   g.gene_name, g.length, s.gDNA, s.CDS_join, s.codon_start, s.translation From Gene g, Sequence s Where g.gene_id = s.gene_id ";

		db = DatabaseAccess();
		result = db.Script_Execute(sql);              
		
		return result #returning result as dictionary
		   


	def AccessSeqData_Gene (self, gene_name):
			
		"""

		This function will search DB based on gene name and return a gene name, gene length,  gDNA sequence, CDS_join, codon start position and translation seq
		which will be used by middle layer to derive CDS, cal codon usage etc
		input = gene_name (exact or partial name ?), sql
		output = a dictionary containing gene_name, length of the gene, gDNA sequence (nucleotide seq), CDS_join, codon start position and translation seq for the querried gene
		
		"""
		# Create SQL statement to find a nucleotide seq, cds start and end postion, cds from Tables Gene and Sequence
		sql = "Select   g.gene_name, g.length, s.gDNA, s.CDS_join, s.codon_start, s.translation From Gene g, Sequence s Where g.gene_id = s.gene_id AND upper(g.gene_name) LIKE upper('%" + gene_name + "%');" 
	  
		db = DatabaseAccess();
		result = db.Script_Execute(sql);
		return result #returning result as dictionary

	

	def AccessRestriction_Enz_Info (self, name):
			
		"""This function will return a queried restriction enzyme name and its cut site 
		input = RE_name (restriction enzyme name)
		output = dict containing RE_name (key) and it's cut_site (value) """
	   
		# Create SQL statement to find a RE_name and cut_site from Table Restrition Enzyme
		sql = "select RE_name, cut_site From   Restriction_enzymes Where upper(RE_name) LIKE upper('%"+ name +"%');"
		db = DatabaseAccess()
		result = db.Script_Execute(sql)
		return result #returning result as dictionary

	
	def AccessRestriction_Enz_List (self):
			
		"""This function will return a list of all restriction enzyme name and their cut sites 
		input = RE_name (restriction enzyme name)
		output = a dict containing all RE_name (key) and their cut_site (value) """
	   
		# Create SQL statement to find a RE_name and cut_site from Table Restrition Enzyme
		sql = "select RE_name, cut_site From   Restriction_enzymes " 
	  
		db = DatabaseAccess();
		result = db.Script_Execute(sql);
		return result #returning result as dictionary



# x = RetriveData()

# # These are the functions to provide the lists
# print(x.AcessGeneList())
# print(x.AccessRestriction_Enz_List());
# print(x.ProductNameList())
# print(x.AccessChromLocList())
# print(x.ProductNameList())
# print(x.AccessSequenceSummary())


# #these are the functions to get a gene name, chromosome loc, accession number, protein product name, Sequence data and Restriction enzyme and cutsite 
# print(x.AccessGeneData('put the gene name here'))
# print(x.AccessAccession_number('put the accession number here'))
# print(x.AccessChromosome_loc('put chromosome loc here'))
# print(x.AccessProduct_name('put product name here'))
# print(x.AccessSeqData_AccNo('put accession number here'))
# print(x.AccessSeqData_Gene('put gene name here'))
# print(x.AccessRestriction_Enz_Info('put the RE name here'))

