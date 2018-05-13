#!/usr/bin/env python3

"""
Program:        chromosome15_gene_browser
File:           businessLogicMainFile.py
Version:        V1.0
Date:           17.04.2018
Function:       Provide a simple file for a front end to work with. See business_logic.py file
                for break down of functions
Copyright:                  Sarah Griffiths
Author:                     Sarah Griffiths
project_collaborators:      Archana Patil, Sergio Ramalli, Fabio Biond
Address:                    Bioinformatics, BBK, London
-------------------------------------------------------------
This program is released under the General use (GNU) Public License
-------------------------------------------------------------
Description:
==============
This programme accepts requests from a web page to query the data base Chromosome15
and processes and returns requested data in Python Variables - see user guide for description
of variables
---------------------------------------------------------------
Usage:
===========
Chromosome15_gene_browser
-----------------------------------------------------------------
Revision History:
=================
V1.0 17.04.2018     Original    BY: SG
v2.0 28.04.2018     Original    BY: SG
v3.0 07.05.2018     Include data access layers BY:SG
v3.1 08.05.2018     final edits BY: SG
"""

import archana as DB
import businessLogic as BL

def getAllGenes():
    """ accesses DB and returns list of all genes A-Z """
    
    gene_list = 'gene' #assigning varibale as functions require an argument
    geneList =DB.RetriveData.AcessGeneList(gene_list)
    return(geneList)

def getAllProteins():
    """ accesses DB and returns list of all proteins A-Z """
    ProteinProductName_list = 'ProteinProductName'
    proteinList =DB.RetriveData.ProductNameList(ProteinProductName_list)
    return (proteinList)

def getAllAccessions():
    """ accesses DB and returns list of all Accessions A-Z """
    accessionNo_list = accessionNo_List
    accessionsList =DB.RetriveData.AccessionNumberList(accessionNo_list)
    return (accessionList)

def getAllChromosomeLocations():
    """ accesses DB and returns list of all chromosome locations """
    Chrom_Loc_List = Chrom_Loc_List
    chromosomeLocationList= DB.RetriveData.AccessChromLocList(Chrom_Loc_List)
    return (chromosomeLocationList)
def getAllEntryData(key,type): 
    """ returns all data for a particular record
    input: key --- genename/accession/protein name/chromsome location
    output accession_number, NCBI_identifier, chromosome_location, protein_product_name
           parsedSequence, codingRegion, mrnaSequence, splitSequence, translatedAndAligned,
           justAminoAcids, codonFrequency, RestrictionEnzymes
           --- see user guide for description of each """
    # access gene DB layer via accession number only and return variables
    basicInfo = DB.RetriveData.AccessAccession_number(type, key)
    return(basicInfo)
    

    sequenceInfo = DB.RetriveData.AccessSeqData_AccNo(type,key)
    
    mainItem = sequenceInfo[0]
    
    CDSjoin = mainItem['CDS_join']
    
    codingRegion = BL.cdsJoin(CDSjoin)

    
    start = int(codingRegion[0])
    end = int(codingRegion[1])
    parsedSequence = mainItem['gDNA']
   
    # access sequence DB layer and return variables

    #processing data with functions created in businessLogic.py - all of them contain 'return' statements so none required here.

    
    codingRegion = BL.codingRegion(start,end,parsedSequence)
    mrnaSequence = BL.translate(codingRegion)
    splitSequence = BL.CodonSequence(mrnaSequence)
    translatedAndAligned = BL.alignseq(splitSequence)
    justAminoAcids = BL.translatedSequence(splitSequence)#check this
    codonFrequency = BL.codonFreq(splitSequence)# need to edit to incorporate total frequencies
                     

    print(codingRegion, mrnaSequence, splitSequence, translatedAndAligned, justAminoAcids, codonFrequency)
    
def restrictionEnzymeCutSites(bases):
    """ input: bases of cut site eg. tcgaa
        return: dictionary of sequence start and end sites and indication of whether or not in coding region """
    dictionary = DB.RetriveData.AccessRestriction_enzymeInfo(name)
    locals().update(dictionary)
    cutSite = cut_site
    cutSiteLocations = BL.restrictionEnzyme(cut_site, start, end, parsedSequence) 
    return (cutSiteLocations) #returned as dictionary


