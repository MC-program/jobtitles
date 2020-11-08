#!/usr/bin/env python
# coding: utf-8


DEFAULT_EXTENSION = "pdf"    # for folder
COMPATIBLE_EXTENSIONS = ["pdf", "txt", "csv", "http", "https"]


import os
import sys

from debug_package import debug, info, warning, error, critical
import file_package
import parser_package




#print("System arguments are:", sys.argv)

if len(sys.argv) < 2:
    print("1. argument: input file name with relative or absolute path")
    print(" This file containts the job-ads in CSV format such as ./jobads/jobads.csv")
    print("2.,3.,etc. optional arguments:")
    print("   NOT IMPLEMENTED. --")
    exit()


if sys.argv[0] == "main.py": # a normal Python call?

    filelist = []
    arglist = []

    if not any([("."+ext in sys.argv[1]) for ext in COMPATIBLE_EXTENSIONS]):
    #if not ".pdf" in sys.argv[1]:
        if not os.path.exists(sys.argv[1]):
            print("Error: Give folder name with input file(s) or file name with extension")
            print("Given name is", sys.argv[1])
            exit()
        else:    ## folder
            filelist = file_package.getAllFiles(sys.argv[1],extension=DEFAULT_EXTENSION)
    else:    # pdf file
        filelist.append(sys.argv[1])

    if len(sys.argv) >1:
        arglist.extend(sys.argv[2:])


    if len(sys.argv) > 2:
        print("Argument for extra parameters / tags found:", sys.argv[2:])
        for arg in sys.argv[2:]:
            if not "###" in arg:
                print("Extra argument not in the format name###value: arg=", arg)
                exit()

    parser_package.init()

    if len(filelist) > 1:
        print("========================================================")
        print("============    Start batch processing    ==============")
        print("Input files are")
        for inputfile in filelist:
            print(inputfile)
        print("========================================================")

    for inputfile in filelist:
        parser_package.run([inputfile]+arglist)

    print("Done with")
    for inputfile in filelist:
        print(inputfile)

    exit()    ######## necessary otherwise it loops again over?!?!?!?!

else:         # Iptyhon Notebook

    parser_package.init()


# EOF
