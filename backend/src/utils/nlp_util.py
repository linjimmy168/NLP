#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 13:05:03 2018

@author: mythri
"""
import re
import string
import nltk
# nltk.download('all')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


exclude = set(string.punctuation)

# Split text to sentences
def sentenceTokenizer(text):
    sentences = re.split('\.|•|�|', text)
    return sentences


# Function to remove punctuatio from a string
def remove_punctuation(sentence):
    try:
        sentence = ''.join(ch for ch in sentence if ch not in exclude)
    except:
        pass
    return sentence

# check if the sentence is title
def checkIfTitle(sentence):
    words = tokenize_words(sentence)
    for i in range(3, len(words)):
        phrase = ' '.join(words[i - 3:i])
        phrase = phrase.replace('and', 'And').replace('to', 'To').replace('for', 'For').replace('the', 'The').replace(
            ' a ', ' A ').replace(' an ', ' An ').replace(' on', ' On').replace('of', 'Of')
        if not phrase.istitle() and len(words[i - 3:]) < 400:
            sentences_notitle = ' '.join(words[i - 3:])
            return sentences_notitle

    return ""

# Check if sentence has atleast one verb
def has_verb(words):
    tags = nltk.pos_tag(words)
    for tag in tags:
        if tag[1].startswith('VB'):
            return True
    return False

def preprocess_data(words):
    words = lower_case(words) # Convert all words to lower case
    words = remove_nonAlphabetic(words) # Remove remaining tokens that are not alphabetic
    words = remove_stopwords(words) # Remove stopwords from sentence
    words = stem_words(words)
    
    return words
    
    
# Returns tokenized words
def tokenize_words(sentence):
    return word_tokenize(sentence)

# Return words converted to lower case
def lower_case(words):
    words_lowercase = [w.lower() for w in words] # Convert to lower case  
    return words_lowercase

# Remove non alphabetic words    
def remove_nonAlphabetic(words):
    words_nonAlphabetic = [word for word in words if word.isalpha()] # Remove remaining tokens that are not alphabetic
    return words_nonAlphabetic

# Remove all stopwords
def remove_stopwords(words):
    stop_words = set(stopwords.words('english'))
    stopwords_removed = [w for w in words if not w in stop_words]
    return stopwords_removed

# Return stemmed words
def stem_words(words):
     porter = PorterStemmer()
     stemmed_words = [porter.stem(word) for word in words]
     return stemmed_words
    