#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 14:14:09 2018

@author: mythri
"""
import os, json
# Check if sentence has less than 150 words
def checkIfShortSentence(words):
    try:
        return  (len(words) <= 150) # Return true if sentence has less than 150 words
    except Exception as e:
        print e


def listToJson(sentences):
    sentences_json = json.dumps(sentences)
    return sentences_json

# creates a folder 
def createfolder(folder_path):
    try:
        os.mkdir(folder_path)
    except Exception as e:
        print e
        
        
def remove_spaces_sentence(sentence):
    sentence = sentence.replace("( ", "(").replace(" )", ")").replace(" ,", ",").replace(" '", "'").replace(" :", ":")
    return sentence