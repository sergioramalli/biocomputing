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

accessLayer = DB.RetriveData();

def getAllGenes():

    """ accesses DB and returns list of all genes A-Z """
    geneList = accessLayer.AcessGeneList()
    return(geneList)

def getAllProteins():

    proteinList =accessLayer.ProductNameList()
    return (proteinList)

def getAllAccessions():

    accessionsList =accessLayer.AccessionNumberList()
    return (accessionList)

def getAllChromosomeLocations():

    chromosomeLocationList= accessLayer.AccessChromLocList()
    return (chromosomeLocationList)

def getAllEntryData(key, searchType): 

    """ returns all data for a particular record
    input: key --- genename/accession/protein name/chromsome location
    output accession_number, NCBI_identifier, chromosome_location, protein_product_name
           parsedSequence, codingRegion, mrnaSequence, splitSequence, translatedAndAligned,
           justAminoAcids, codonFrequency, RestrictionEnzymes
           --- see user guide for description of each """
    # access gene DB layer via accession number only and return variables

    returnObject = {};

    if searchType == 'gene': 

        basicInfo = accessLayer.AccessGeneData(key);

        xx = 0;
        for x in basicInfo:

            sequenceInfo = accessLayer.AccessSeqData_AccNo(x['accession_number'])[0]
            returnObject[xx] = {
                # 'sequenceInfo' :retrieveSequenceAnalysis(sequenceInfo),
                'basicInfo' : basicInfo[0]
            };
            xx += 1;

            pass

        pass;
        
    elif searchType == 'accession':

        basicInfo = accessLayer.AccessAccession_number(key);

        sequenceInfo = accessLayer.AccessSeqData_AccNo(key)[0]
        returnObject[0] = {
            # 'sequenceInfo' :retrieveSequenceAnalysis(sequenceInfo),
            'basicInfo' : basicInfo[0]
        };

    elif searchType == 'protein_product_name':

        basicInfo = accessLayer.AccessProduct_name(key);

        xx = 0;
        for x in basicInfo:

            sequenceInfo = accessLayer.AccessSeqData_AccNo(x['accession_number'])[0]
            returnObject[xx] = {
                # 'sequenceInfo' :retrieveSequenceAnalysis(sequenceInfo),
                'basicInfo' : basicInfo[0]
            };
            xx += 1;

            pass

        pass; 

    elif searchType == 'chromosome_location':

        basicInfo = accessLayer.AccessChromosome_loc(key);

        xx = 0;
        for x in basicInfo:

            sequenceInfo = accessLayer.AccessSeqData_AccNo(x['accession_number'])[0]
            returnObject[xx] = {
                # 'sequenceInfo' :retrieveSequenceAnalysis(sequenceInfo),
                'basicInfo' : basicInfo[0]
            };
            xx += 1;

            pass

        pass; 

    return returnObject;


def retrieveSequenceAnalysis(sequenceInfo):
    """ The functions access all of analysis from sarah's BL file import and return all analysis of the file
    input: Sequence 
    output parsedSequence, codingRegion, mrnaSequence, splitSequence, translatedAndAligned,
           justAminoAcids, codonFrequency
           --- see user guide for description of each """

    try:

        CDSjoin = sequenceInfo['CDS_join'];
        codingRegion = BL.cdsJoin(CDSjoin)

        if not codingRegion[0].isnumeric():
            print(codingRegion);
            raise ValueError('couldnt find coding region of gene');

        if not codingRegion[1].isnumeric():
            raise ValueError('couldnt find coding region of gene');


        start = int(codingRegion[0])
        end = int(codingRegion[1])
        parsedSequence = sequenceInfo['gDNA']

        #processing data with functions created in businessLogic.py - all of them contain 'return' statements so none required here.
        codingRegion = BL.codingRegion(start,end,parsedSequence)
        mrnaSequence = BL.translate(codingRegion)
        splitSequence = BL.CodonSequence(mrnaSequence)
        translatedAndAligned = BL.alignseq(splitSequence)
        justAminoAcids = BL.translatedSequence(splitSequence)#check this
        codonFrequency = BL.codonFreq(splitSequence)# need to edit to incorporate total frequencies

        return({
            'error' : False,
            'codingRegion' : codingRegion, 
            'mRnaSequence' : mrnaSequence, 
            'splitSequence' : splitSequence, 
            'translatedAndAligned' : translatedAndAligned, 
            'justAminoAcids' : justAminoAcids,
            'codonFrequency' : codonFrequency,
        });

    except Exception as e:

        return({
            'error' : e,
            'codingRegion' : '', 
            'mRnaSequence' : '', 
            'splitSequence' : '', 
            'translatedAndAligned' : '', 
            'justAminoAcids' : '',
            'codonFrequency' : '',
        });


    
def restrictionEnzymeCutSites(bases):

    """ input: bases of cut site eg. tcgaa
        return: dictionary of sequence start and end sites and indication of whether or not in coding region """
    dictionary = accessLayer.AccessRestriction_enzymeInfo(name)
    locals().update(dictionary)
    cutSite = cut_site
    cutSiteLocations = BL.restrictionEnzyme(cut_site, start, end, parsedSequence) 
    return (cutSiteLocations) #returned as dictionary

