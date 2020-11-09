#!/usr/bin/env python
# coding: utf-8



import os
import sys
import csv
import re

from fuzzywuzzy import fuzz

from debug_package import *






###############################################################################
#################                                            ##################
#################                 search                     ##################
#################                                            ##################
###############################################################################



from fuzzysearch import find_near_matches
from fuzzywuzzy import process

def fuzzySearch(strShort, strLong, threshold):
    '''
    Fuzzy matches 'strShort' in 'strLong' and returns list of 
    tuples of (word,index)
    '''
    for word,percent in process.extractBests(strShort, (strLong,), score_cutoff=threshold):
        #print('fuzzy={}'.format(word))
        for match in find_near_matches(strShort, word, max_l_dist=5):
            match = word[match.start:match.end]
            #print('match={}'.format(match))
            index = strLong.find(match)
            yield (match,index,percent)

    #large_string = "thelargemanhatanproject is a great project in themanhattincity"
    #query_string = "manhattan"
    #gen = fuzzySearch(query_string,large_string,80)
    #for gen1 in gen:
    #    print(gen1)

def fuzzySearch2(strShort, strLong, threshold):
    """
    Similar to fuzzySearch but with fuzzywuzzy

    Does not return index. Just constant -1
    """

    hitrate = fuzz.partial_ratio(strShort,strLong)     # shorter n-substring against
                                                # all other n-substrings

    if hitrate >= threshold:
        yield (strShort,-1,hitrate)

