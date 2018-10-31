#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 17:17:31 2018

@author: mythri
"""

import json

def get_base_filename(filename, separator):
    try:
        basename,_ext = filename.split(separator)
        return basename
    except Exception as e:
        print e
        
        
def read_file(file_path, permisson):
    with open(file_path, permisson) as fopen:
        try:
            text = fopen.read()
            return text
        except IOError:
            print "Error: " + file_path + " does not appear to exist."
            
            
def write_file(data, file_path, permisson):
    with open(file_path, permisson) as fopen:
        try:
            text = fopen.write(data)
            return text
        except IOError:
            print "Error: " + file_path + " does not appear to exist."
    

def json_dump(data, file_path, permission):  
    with open(file_path, permission) as fopen:
         try:
             json.dump(data,fopen)
         except IOError:
            print "Error: " + file_path + " does not appear to exist."
    
    
# Extract data from json files 
def json_loads(file_path, permission):
    with open(file_path, permission) as data_file:
        try:
            data = json.load(data_file)
            return data
        except IOError:
            print "Error: " + file_path + " does not appear to exist."
    
    
# Extract data from json files and decode
def json_loads_decode(file_path, permission):
    with open(file_path, permission) as data_file:
        try:    
            return _byteify(json.load(data_file, object_hook=_byteify),ignore_dicts=True)
        except IOError:
            print "Error: " + file_path + " does not appear to exist."


def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

