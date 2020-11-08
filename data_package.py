#!/usr/bin/env python
# coding: utf-8



import os
import sys
import csv
import re

from debug_package import *






###############################################################################
#################                                            ##################
#################                 search                     ##################
#################                                            ##################
###############################################################################



from fuzzysearch import find_near_matches
from fuzzywuzzy import process

def fuzzySearch(qs, ls, threshold):
    '''fuzzy matches 'qs' in 'ls' and returns list of 
    tuples of (word,index)
    '''
    for word,percent in process.extractBests(qs, (ls,), score_cutoff=threshold):
        #print('fuzzy={}'.format(word))
        for match in find_near_matches(qs, word, max_l_dist=5):
            match = word[match.start:match.end]
            #print('match={}'.format(match))
            index = ls.find(match)
            yield (match,index,percent)

    #large_string = "thelargemanhatanproject is a great project in themanhattincity"
    #query_string = "manhattan"
    #gen = fuzzySearch(query_string,large_string,80)
    #for gen1 in gen:
    #    print(gen1)


