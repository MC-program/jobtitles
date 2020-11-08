#!/usr/bin/env python
# coding: utf-8


import logging


################################################################
##                       DEBUGGING
################################################################

logging.basicConfig(level=logging.DEBUG)
g_debugLevel = logging.DEBUG



def setDebugLevel(level):
    """
    Set debug level: logging.DEBUG ... logging.CRITICAL

    We use a the global logging module, so this is not only this class
    """
    global g_debugLevel

    level = int(level)

    g_debugLevel = level
    logging.basicConfig(level=level)

    print("setDebugLevel(): Set global logging level to", g_debugLevel)


def printDebugLevel():
    """
    Print debug level set by setDebugLevel()

    Inform about levels as well
    """
    global g_debugLevel

    print("debugLevel(): level is", g_debugLevel)

def debug(*msg):
    """ Return anchor object with highest hitrate

    @return ANCHOROBJ (type1)
    """
    global g_debugLevel

    if g_debugLevel > logging.DEBUG:     # for IPtython
        return

    msgTotal = ""
    for arg in msg:
        msgTotal += str(arg) +" "
    logging.debug(msgTotal)

def info(*msg):
    global g_debugLevel

    if g_debugLevel > logging.INFO:     # for IPtython
        return

    msgTotal = ""
    for arg in msg:
        msgTotal += str(arg) +" "
    logging.info(msgTotal)
    
def warning(*msg):
    global g_debugLevel

    if g_debugLevel > logging.WARNING:     # for IPtython
        return

    msgTotal = ""
    for arg in msg:
        msgTotal += str(arg) +" "
    logging.warning(msgTotal)

def error(*msg):
    global g_debugLevel

    if g_debugLevel > logging.ERROR:     # for IPtython
        return

    msgTotal = ""
    for arg in msg:
        msgTotal += str(arg) +" "
    logging.error(msgTotal)

def critical(*msg):
    global g_debugLevel

    if g_debugLevel > logging.CRITICAL:     # for IPtython
        return

    msgTotal = ""
    for arg in msg:
        msgTotal += str(arg) +" "
    logging.critical(msgTotal)



STRING_LENGTH = 30             # length of string to output
ITERABLE_LENGTH = 10           # number of elements to output

def getSnippet(textable):
    """
    Return first 10 elements or some characters of string

    textable is iterable or string
    """
    def isIterable(obj):
        """
        Helper to check the obj is iterable
        """
        try:
            iter(obj)
        except Exception:
            return False
        else:
            return True

    def shorten(string):
        """
        Helper to cut down to max of 40 characters
        """
        #ret = ""
        string = str(string)
        if len(string) > STRING_LENGTH:
            return string[:STRING_LENGTH] +".."
        return string
    return textable

    if isinstance(textable,str):
        return shorten(textable)
    elif isIterable(textable):
        return str([shorten(e) for e in textable[:min(len(textable),5)]])


