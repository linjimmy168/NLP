#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:40:43 2018

@author: mythri
"""

import os, sys

#root = os.path.abspath('../../../linkSDGs')
root = os.path.abspath('../linkSDGs')
print 'Working directory--------->' + root
sys.path. append(os.path.abspath(os.path.dirname(root)))
from src import convert_pdf_to_text, sdg_classifier, goals_summary

def main(documents_name):
    data_path =  os.path.abspath(root) + "/data" # Place where all data is stored
    pdfs_path = data_path + '/pdfs/' + documents_name # Place where uploaded documents are stored
    fixed_pdfs_path = pdfs_path+'_fixed_name/' # Place where files with fixed names of uploaded documents are stored
    labelled_path = data_path + '/SDG_classified/'+ documents_name + '/' # Place where labelled data is stored
    try:
        convert_pdf_to_text.rem_space(pdfs_path+'_pdfs/',fixed_pdfs_path) # Rename files to remove space in filenames
        convert_pdf_to_text.iterate_folder(fixed_pdfs_path) # Convert each pdf file in folder to text
        sdg_classifier.label_data(fixed_pdfs_path, labelled_path ) # Label the data
        goals_summary.iter_SDGsCombination(labelled_path, data_path+'/visualization/SDG_summary/', labelled_path+"/nexus/" , documents_name)
        #goals_summary.iter_SDGsCombination(labelled_path, data_path+'/SDG_summary/' , documents_name)

    except Exception as e:
         print e


if __name__ == '__main__':
    main(sys.argv[1])
