# -*- coding: utf-8 -*-
import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__)))
from utils import util, file_util, other_utils

sentences = []

# Extracts sentences from text file and labels all the SDG mentioned in each sentence
def label_data(source, destination):
    
    if not os.path.isdir(destination):
        other_utils.createfolder(destination) # Check if destination folder exists if not create
        
    print('\n......Classifying sentences.......')
    # Get all the text file in folder to be labelled
    source_list = [filename for filename in os.listdir(source) if filename.endswith(".txt")]
    json_file_list = [filename for filename in os.listdir(destination) if filename.endswith(".json")]
    for filename in source_list:
        base_filename, _ext = filename.split('.txt') # Get base filename
        json_filename = base_filename + '.json' # name labelled json file to be stored
        # Consider only text files that are not already labelled
        if json_filename not in json_file_list:            
            document = file_util.read_file(source + filename, 'r') # Get text from the file
            sdg_pairs+ =  util.get_SDGs_pair(destination+'nexus/')
            sentences, updated_sdg_pair = util.filterSentences(document, filename, sdg_pairs) # Returns labelled sentences for given text file
            file_util.json_dump(sentences, destination+json_filename, 'w+')
            file_util.json_dump(updated_sdg_pair, destination+'nexus/'+'sdg_pairs.json', 'w+')
            
    print('\n....Finished classifying sentences.....')


'''
if __name__ == '__main__':
   label_data('/Users/mythri/Documents/Codes/linksdgs/data/pdfs/Test_fixed_name/','/Users/mythri/Documents/Codes/linksdgs/data/SDG_classified/Test/')
'''
