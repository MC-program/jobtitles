#!/usr/bin/env python
# coding: utf-8

import os
import sys
import csv

from debug_package import * # debug, info, warning, error, critical
from data_package import *



class CFileCache:
    '''
    Class for caching file content to a key

    Pay attention to the format of the file (outside).
    '''

    #def getFileContent(path):
    def __init__(self, debugOutput=False):
        self.keyToContent = {}
        info("CFileCache.__init__()")

    def __del__(self):
        info("CFileCache.__del__()")

    def isThere(self,key):
        return key in self.keyToContent

    def get(self,key):
        if not key in self.keyToContent:
            return None
        return self.keyToContent[key]

    def set(self,key,content):
        if key in self.keyToContent:
            raise Exception("Content already defined")
        self.keyToContent[key] = content

g_fileCache = CFileCache()


def getAllFiles(path):
    return []


def getAllFiles(folder, extension):
    return []


def readRowsAndCols(filename,
                    removePunctuation,
                    makeLower,
                    delimiter=",",
                    encoding="utf8",
                    debugOutput=False):
    """
    Read in CSV as 2d array:
    """

    rows = []

    try:

        rows2 = g_fileCache.get(filename)
        if rows2:
            return rows2

        with open(filename, encoding=encoding) as csvFile:
            csvReader = csv.reader(csvFile, delimiter=delimiter)  #iterator obj

            for row in csvReader:

                rowtemp = []
                for col in row:

                    if makeLower:
                        col = col.lower()

                    if removePunctuation:
                        col = removePunctuationFromText(col).strip()

                    if len(col):
                        rowtemp.append(col)

                if len(rowtemp):  # export row?
                    if rowtemp in rows:
                        _=0
                    else:
                        rows.append(rowtemp)

    except Exception as e:
        raise Exception("readRowsAndCols(): error:", e)
        #pass
        
        return []

    if rows != None and len(rows):
        g_fileCache.set(filename, rows)

    return rows



def readContentFlat(path,
                    filename,
                    language   ="",
                    delimiter  =",",
                    encoding   ="utf8",
                    makeLower  =True,
                    addEnglishContent=False,
                    removePunctuation=True,
                    debugOutput=False):
    """
    Read-in the file(s) according to readRowsAndCols() and return it as a flat array
    """
    filenames = []

    if len(language): # language set
        filenames.append(path +language +"-" +filename)
        if addEnglishContent and language != "english":
            filenames.append(path +"english" +"-" +filename)
    else:
        filenames.append(path +filename)

    contentFlat = []

    try:
        for filename in filenames:

            rowsCols2 = readRowsAndCols(filename=filename,
                                        removePunctuation=removePunctuation,delimiter=delimiter,
                                        encoding=encoding, makeLower=makeLower,
                                        debugOutput=debugOutput) 
            rowsCols2 = [i for sub in rowsCols2 for i in sub] # it is a list of a list -> flatten

            for word in rowsCols2:
                if not word in contentFlat: # extend?
                    contentFlat.append(word)

    except Exception as e:
        critical("readContentFlat(): error:", e, "for filename", filename)
        assert False

    return contentFlat




def readContentByRow(path,
                    filename,
                    language   ="",
                    delimiter  =",",
                    encoding   ="utf8",
                    makeLower  =True,
                    addEnglishContent=False,
                    removePunctuation=True,
                    debugOutput=False):
    """
    Read-in the file(s) according to readRowsAndCols() and return it as a flat array
    """

    contentFlat = []

    try:

        rowsCols2 = readRowsAndCols(filename=path+filename,
                                    removePunctuation=removePunctuation,delimiter=delimiter,
                                    encoding=encoding, makeLower=makeLower,
                                    debugOutput=debugOutput) 

        for row in rowsCols2:
            contentFlat.append("")
            for col in row:
                if len(contentFlat[-1]):
                    contentFlat[-1] += ","
                contentFlat[-1] += col

    except Exception as e:
        critical("readContentFlat(): error:", e, "for filename", filename)
        assert False

    return contentFlat

# Read row by row
# with open('Book8.csv') as fp:
# for line in fp:
    # print line

def writeFile(filename, content):

    #with open(self.getXMLPath(), "wb") as f:       # bytes
    with open(filename, "w") as f:
        f.write(content)
        print("writeFile(): file exported:", filename)


