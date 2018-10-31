#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 16:16:50 2017

@author: mythri
"""
import os
import tika
tika.initVM()
from tika import parser

# Iterate pdf directory and remove replace characters from filename
def rem_space(source, destination):
    if not os.path.exists(destination):
        os.makedirs(destination) 
    file_list = os.listdir(source)
    try:
        for i in range(len(file_list)):
            os.rename(source + file_list[i] , destination + rem_space_filename(file_list[i]))
        print(' ......done removing whitespace from filenames ...')
    except Exception as e:
         print e

# Remove spaces from pdf filename
def rem_space_filename(filename):
    return ''.join(filename.split())

# Convert all documents in folder to text
def iterate_folder(folderpath):
    print '\nConverting documents to text'
    for filename in os.listdir(folderpath):
        if filename.endswith(".pdf"):
            base_file, _ext = filename.split('.pdf')
            destination_filename = base_file + '.txt'
            if destination_filename not in os.listdir(folderpath):
                parsedPDF= parser.from_file(folderpath + filename)
                text = parsedPDF["content"]
                fopen = open(folderpath+'/'+destination_filename, 'wb')
                fopen.write(text.encode('utf-8'))

    print("Finished documents pdfs to text\n")


