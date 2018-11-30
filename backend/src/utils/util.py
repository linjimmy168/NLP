#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:01:34 2018

@author: mythri
"""
import os, sys
import sdgs_lookup
sys.path.append(os.path.join(os.path.dirname(__file__)))
from utils import nlp_util, file_util, other_utils

sdgs_dict = sdgs_lookup.stemmed_sdgs
targets_dict = sdgs_lookup.stemmed_targets

def get_SDGs_pair(nexus_folderpath):
    try:
        sdg_pairs = []
        # Return an empty object if the sdg_pair object does not exist
        if os.path.isfile(nexus_folderpath+'sdg_pairs.json'):
            sdg_pairs = file_util.json_loads(nexus_folderpath+'sdg_pairs.json', 'r')
        else:
            if not os.path.isdir(nexus_folderpath):
                other_utils.createfolder(nexus_folderpath)
        
        return sdg_pairs 
    except Exception as e:
        print e
        
        
def filterSentences(text, filename, sdg_pairs):
    filename = filename.replace('.txt', '.pdf') # Rename the source with pdf ext
    filtered_sentences = {}
    filtered_sentences[filename] = []
    
    text = text.replace("-\n", "").replace("\n", " ")
    sent_text = nlp_util.sentenceTokenizer(text)
                  
    for i in range(len(sent_text)):
        sentence = nlp_util.remove_punctuation(sent_text[i]) # Remove punctuation
        words = nlp_util.tokenize_words(sentence) # split into words
        short_sentence = other_utils.checkIfShortSentence(words) # True if sentence is lesser than 150 words

        if short_sentence:
            verb_sentence = nlp_util.has_verb(words) # Sentence must have atleast one verb
            if verb_sentence:
                sdgs_mentioned, _targets= matchSDGs(words, False) 
                sentences_notitle = nlp_util.checkIfTitle(sent_text[i].decode('utf-8'))

                if len(sdgs_mentioned) >= 2 and len(sdgs_mentioned) <= 4 and sentences_notitle != "":
                    filtered_sentences[filename].append(
                            {'Sentence': sentences_notitle.strip(), 
                             'SDGs': sdgs_mentioned 
                             }
                            )
                    
                    sdg_pairs = countSDGPairs(sdgs_mentioned, sdg_pairs) # Keep count of SDG co-occurrence

    return filtered_sentences, sortCount(sdg_pairs)



def countSDGPairs(sdgs_mentioned, sdg_pairs):
    for i in range(len(sdgs_mentioned)-1):
        for j in range(i+1, len(sdgs_mentioned)):
            
            if sdgs_mentioned[i] != sdgs_mentioned[j]:
                pair = [sdgs_mentioned[i], sdgs_mentioned[j]]
                pair_exists = False
                
                for k in range(len(sdg_pairs)):
                    if pair[0] in sdg_pairs[k][0] and pair[1] in sdg_pairs[k][0]:
                        sdg_pairs[k][1] += 1
                        pair_exists = True

                if not pair_exists:
                    sdg_pairs.append([pair, 1])

    return sdg_pairs


def sortCount(data):
    return sorted(data, key=getCount, reverse=True)


def getCount(pair):
    return pair[1]



# Match SDGs by sdgs look up dictionary. Also matchas SDG on target level if find_targets is set to True 
def matchSDGs(sent_words, find_targets):
    sdgs_mentioned = []
    targets_mentioned = []

    processed_words = nlp_util.preprocess_data(sent_words)
    # Match main SDGs
    
    sdgs_mentioned = lookup(processed_words, sdgs_dict)
    # Match corresponding SDGs on target level
    if find_targets:
        for each in sdgs_mentioned:
                targets = lookup(processed_words, targets_dict[each])
                for target in targets:
                    targets_mentioned.append(target)
    
    return sdgs_mentioned, targets_mentioned
    


def lookup(sent_words, dictionary):
    labels = []

    for key in dictionary.keys():
       keywords =  [nlp_util.tokenize_words(keyword) for keyword in dictionary[key]]
       for key_phrase in keywords:
           is_present = key_phrase[0] in sent_words
           for i in xrange(1, len(key_phrase)):
               is_present &= key_phrase[i] in sent_words
               
           if(is_present): 
               labels.append(key)
               break 
    
    return labels













'''
# Match SDGs by sdgs look up dictionary
def matchSDGs(sent_words):
    sdgs_mentioned = []

    words = [w.lower() for w in sent_words] # Convert to lower case    
    words = [word for word in words if word.isalpha()] # Remove remaining tokens that are not alphabetic
    stop_words = set(stopwords.words('english'))
    words = [w for w in words if not w in stop_words]
    
    for sdg in sdgs.items():
        for key in sdg[1]:
            if key in sent_words and sdg[0] not in sdgs_mentioned:
                sdgs_mentioned.append(sdg[0])

    return sdgs_mentioned, words

# Match corresponding SDGs  on target level
def matchTargets(sdgs_matched, words):
    targets_mentioned = []
    for target in targets.items():
        for key in target[1]:
            if key in words and target[0] not in targets_mentioned and matchSDGwithTarget(sdgs_matched,target[0]):
                targets_mentioned.append(target[0])

    return targets_mentioned


def matchSDGwithTarget(sdgs_matched, target):
    for i in range(len(sdgs_matched)):
        sdgnumber = target[0:target.find('.')]
        if sdgs_matched[i] in sdgnumber:
            return True

    return False

'''

