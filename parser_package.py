#!/usr/bin/env python
# coding: utf-8

ENCODING = "UTF-8"

import os
import json
import sys
from datetime import date
from collections import Counter
import re       # extract all the numbers from a string
from operator import itemgetter
import io                      ###### UTF-8 files
import string as STRING


from debug_package import logging, debug, info, warning, error, critical, setDebugLevel, printDebugLevel
import debug_package                # add missing members
from data_package import *
import file_package



#XML export
#import xml.etree.ElementTree as XMLExport


###############################################################################
#################                                            ##################
#################                  main class                ##################
#################                                            ##################
###############################################################################

class CDocMyPDF:
    '''
    Class for processing PDF file with the Fitz / PyMyPDF.
    '''

    """
        not implemented.
    """

# CDocMyPDF end.


class CDocMyCSV:
    '''
    Class for processing a CSV file

    Use case is now:
    Job advertisments in the CSV and lookup for job title. Found job titles get exported.

    See self.parseDocument()
    '''

    #def getFileContent(path):
    def __init__(self,
                 inputFile,
                 language=None):

        if inputFile != "":
            logFile = os.path.splitext(inputFile)[0] +".log"
            print("CDocMyCSV: inputFile=", inputFile, "; logging to", logFile)
            logging.basicConfig(filename=logFile,level=logging.DEBUG)  # all

        info("CDocMyCSV.__init__(): inputFile=", inputFile)

        #self.inputFile    = inputFile
        self.inputFile    = os.path.abspath(inputFile)                        # input pdf file &path
        self.outputPath   = os.path.dirname(self.inputFile)                   # path only
        self.filename     = os.path.splitext(os.path.basename(inputFile))[0]  # without extension


        self.text         = []
        self.jobTitles    = []

        #self.readDocument()  # Convert jobtitle, jobads file into files

        self.parseDocument()

        #self.setLanguage(language)        # set or find language
        #self.extractor = URLExtract()



    def __del__(self):
        info("CDocMyCSV.__del__()")

        if hasattr(self,"doc"):
            self.doc.close()



    ### =================================================================== 
    ### =================================================================== 

            

    ### ___________________  get & set  _____________________



    def readDocument(self):
        """
        Only to read the raw file of the exercise.
        """

        jobs, ads = [],[]
        rowsColsRaw = file_package.readRowsAndCols(filename=self.inputFile,
                                                   removePunctuation=False,
                                                   makeLower=True)
        for rows in rowsColsRaw:
            jobs.append(str(rows[0]))
            ads.append(str(rows[1]))

        i = 0


        jobsExported = ""
        for datum in ads:
            if len(jobsExported):
                jobsExported += ",\n"
            jobsExported += "\""+datum+"\""

        file_package.writeFile("./jobads/jobads.csv",jobsExported)

        return rowsColsRaw
    # getTextFromCSV() END.



    def parseDocument(self):
        """
        Export found job titles in the input file to the output file jobs_found.csv
        
        Format of jobs_found:
        <nr of job ad in input file>, <job title found>, <index/coordinate in job ad>, <job ad for reference>

        if nothing found, <job title found> gets NOT FOUND, and
        <index/coordinate> gets -1
        """
        jobads, jobtitles = [], []

        ### Load job title database
        jobtitles = file_package.readContentFlat(path="",
                                                 filename="./jobs/jobs.csv",
                                                 removePunctuation=False,
                                                 makeLower=True)

        ### Load input file to process
        jobads = file_package.readContentFlat(path="",
                                              filename=self.inputFile,
                                              removePunctuation=False,
                                              makeLower=True)
        #debug(jobtitles)

        findings = ""

        #for jobNr,ad in enumerate(jobads[:10]):
        for jobNr,ad in enumerate(jobads[:]):

            hitMax = 0
            matchBest = "NOT FOUND,-1"

            for job in jobtitles:
                results = fuzzySearch(job,ad,50)

                matches = [i for i in results]    # Format: 
                #debug("matches"); debug(matches)

                for match in matches:
                    hit = match[2]
                    
                    if hit>hitMax:
                        hitMax = hit
                        matchBest = "\"" +str(match[0]) +"\"," +str(match[1])
                        #debug(str(jobNr)+". job="+job,"in ad?", match)
                    #if matched:
                    #    debug("...ad=",ad)

            debug("parseDocument(): best job found in row="+ str(jobNr) +", (match,pos)=("+matchBest+")")
            findings += str(jobNr) +"," +matchBest +",\"" +ad +"\",\n"    # 1 line == 1 best match

        file_package.writeFile(filename="./jobs_found.csv",content=str(findings))

        #matched = [i for i in fuzzySearch(job, "software engineers",20)]
        #if matched: debug("matched=", matched, "in the field", ad)

        #if i>10: break


###############################################################################
#################                                            ##################
#################                   start-up                 ##################
#################                                            ##################
###############################################################################


def init():
    """
    Initialize class for use
    """

    setDebugLevel(logging.DEBUG)
    printDebugLevel()




def run(args):
    """
    Initialize class for use
    """

    argsActual = []
    argsTag = []

    info("run() with args=", args, "...")

    argsActual = args[0].split("###")   ### [0]=tag, [1,2,...]=attributes
    

    #if len(argsActual) > 1:
    #    print("language parameter found in the first argument:", argsActual[1])
    assert len(argsActual)==1, "argument " +args[0]+ " cannot provide ###"

    if len(args) > 1:
        argsTag = args[1:]
        for arg in argsTag:
            assert "###" in arg, "run(): Provide XML tag arguments in the format name###value"
        print("run(): tag argument(s) found:", argsTag)

    inputFile = argsActual[0]

    runMode    = ""        # optional arguments
    language   = ""
    outputPath = ""
    debugLevel = ""
    exportArrays = []

    # Iterate extra arguments = extra tags in the output
    for arg in argsTag:

        nameValuePairs = arg.split("###")   ### [0]=tag, [1,2,...]=attributes
        nPairs = len(nameValuePairs)

        exportArray = []        ### format: [{tag:value}]
                                ###     or  [{tag:value}, {attributes:values}]

        assert nPairs % 2 == 0, "run(): Provide name-value pairs only in tag argument"   # even number

        if nameValuePairs[0] == "mode":
            runMode = nameValuePairs[1]
            continue
        elif nameValuePairs[0] == "language":
            language = nameValuePairs[1]
            continue
        elif nameValuePairs[0] == "outputpath":
            outputPath = nameValuePairs[1]
            continue
        elif nameValuePairs[0] == "debug":
            debugLevel = nameValuePairs[1]
            continue


    ########################
    ### document object according to type

    ### run
    if ".pdf" in inputFile:

        assert False, "No compatible input file extension"
        exit()

    elif ".csv" in inputFile:            ### cvs

        """
        outputs:
        parseDocument(): best job found in row=0, (match,pos)=("electricien d'exploitation (f/h)",0)
        parseDocument(): best job found in row=1, (match,pos)=("business analyst sap",0)
        parseDocument(): best job found in row=3, (match,pos)=("java software engineers",0)
        ...
        """

        if len(language):
            assert language == "english" or language == "german", "provide valid language"
            document = CDocMyCSV(inputFile, language)
        else:
            document = CDocMyCSV(inputFile)

        #see     readDocument


        #for row in document.text[:10]:
            #found = row[1].find(row[0])
            #if found != -1:
                #print(row[0], "at pos", found, "until", found+len(row[0]))

    elif "http:"  in inputFile or \
         "https:" in inputFile:            ### web

        assert False, "No compatible input file extension"
        exit()

    elif ".txt" in inputFile:

        assert False, "No compatible input file extension"
        exit()

    else:
        assert False, "No compatible input file extension"
        exit()

    # display the XML flat export file (Solr) ...
    #with open(document.getXMLPathFlatFile(), "r") as f:
    #    ("Content of export file", document.getXMLPathFlatFile()+ ":")
    #    (f.read())


