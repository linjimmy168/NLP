# -*- coding: utf-8 -*-
"""
Created on Thu Jan 9 10:43:06 2018

@author: mythri
"""
import os, sys, json
import requests
import time
import progressbar
sys.path.append(os.path.join(os.path.dirname(__file__)))
from utils import util, file_util, other_utils, sdgs_lookup, nlp_util

# api-endpoint
url = 'http://ec2-18-216-74-205.us-east-2.compute.amazonaws.com:9090'
#url = 'http://localhost:9090'

data = []
sdgs_dict = sdgs_lookup.stemmed_sdgs
targets_dict = sdgs_lookup.stemmed_targets 

# Get summary for all combinations of SDG links with each source file
def iter_SDGsCombination(source, destination, nexus_folderpath, result_filename):
    summary = []  # Final summary sentences extracted from all sentences
    
    source_file_list = [json_file for json_file in os.listdir(source) if json_file.endswith(".json")] # List of classified json files
    
    sdg_pairs = file_util.json_loads_decode(nexus_folderpath+"sdg_pairs.json", "r") # Load unique SDG pairs

    nexus = get_nexus(sdg_pairs) # Get nexus and it's keywords
  
    if not os.path.isdir(destination+result_filename):
        other_utils.createfolder(destination+result_filename)
    
    print '\nGetting summary of all documents'

    for filename in source_file_list: # iterate all source files
        # Iterate file that are not already summarized
        if filename not in os.listdir(destination+result_filename):
            
            file_summary = []
            source_pdf = file_util.get_base_filename(filename,".json") + ".pdf"
            data =  file_util.json_loads(source+filename, 'r') # Get labelled sentence of file
      
            for x in xrange(0 ,len(nexus)): # iterate all combinaiton of linked SDGs
                sdgs = nexus[x]['nexus'] # SDG pair on which files are summarized 
                keywords = nexus[x]['keywords'] # SDG pair keywords for summarization
                
                text = get_filetext(data[source_pdf], sdgs) # Get sentences from belonging to sdg-pair
               
                summary_component = summary_components(keywords, text)
                summ = json.loads(get_summary(summary_component)) # Get summary
                summ_sentences = summ["summary"].split("(...)") # Split summary lines
    
                for sentence in summ_sentences:
                    summary_chunks = {}
                    if not sentence.strip().isspace() and sentence.strip() != '':
                        sentence = other_utils.remove_spaces_sentence(sentence)
                        summary_chunks['text'] = sentence
                        summary_chunks['nexus'] = nexus[x]['nexus']
                        summary_chunks['source'] = source_pdf
                        file_summary.append(summary_chunks)
            
            final_file_summary = filter_duplicate_text(file_summary)
            file_util.json_dump(final_file_summary, destination + result_filename + '/' + filename , 'w+')
        
    
    # Put summary of all files together
    for filename in source_file_list:
        data = file_util.json_loads(destination + result_filename + '/' + filename, 'r')
        for summary_chunk in data:
            summary.append(summary_chunk)
    file_util.json_dump(summary, destination + result_filename + '_summary.json', 'w+')
    file_util.json_dump(sdg_pairs, destination + result_filename + '_SDGsPairs.json', 'w+')
    
    
    print '------------Finished Summarization--------------'



# filter duplicate sentences from summary
def filter_duplicate_text(summary):
    seen_text = set()
    new_summary = []
    for x in xrange(len(summary)):
        text = summary[x]['text']
        words = nlp_util.tokenize_words(text)
        if text not in seen_text:
            sdgs_mentioned, targets_mentioned = util.matchSDGs(words, True) # Fing SDGs mentioned in sentence
            summary[x]['SDGs'] = sdgs_mentioned
            summary[x]['Targets'] = targets_mentioned

            new_summary.append(summary[x])
            seen_text.add(text)
    return new_summary
    


# Getting source filename from data
def get_filename(data_chunk):
    if data_chunk:
        return data_chunk[0]['Source']


# Extract text belonging to same file source
def get_filetext(data, sdgs):
    text = ''
    for each in data:
        if sdgs[0] in each['SDGs'] and sdgs[1] in each['SDGs']:
            text += each['Sentence'] + '. ' # Join all sentences
    return text


def get_nexus(links):
    linkedSDG = []
    for x in xrange(len(links)):
        linkSDGs = {}
        linkSDGs['nexus'] = links[x][0]
        linkSDGs['keywords'] = sdgs_lookup.summary_keywords[links[x][0][0]] + ' ' +  sdgs_lookup.summary_keywords[links[x][0][1]] # Combine keywords of linked SDGs
        linkedSDG.append(linkSDGs)
    return linkedSDG


# Get summary with api call to Summarizer application
def get_summary(summary_component):
    global url
    s = requests.Session()
    try:
        s.get(url + '/set/sessioncookie/123456789')
        r = s.post(url = url, data = json.dumps(summary_component), timeout = None )
        return r.text
    except requests.exceptions.RequestException as e:
        print e


# Input for Summarization
def summary_components(keywords, text):
    summary_components = {    # JSON data to be sent to Summarizer application on Nifi
            'keywords' : keywords,
            'text' : text
            }
    return summary_components

if __name__ == '__main__':
    iter_SDGsCombination('/Users/mythri/Documents/Codes/linksdgs/data/SDG_classified/Test/', '/Users/mythri/Documents/Codes/linksdgs/data/visualization/SDG_summary/', '/Users/mythri/Documents/Codes/linksdgs/data/SDG_classified/Test/nexus/','Test')
    