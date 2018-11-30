# -*- coding: utf-8 -*-
import os, sys
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__)))
from utils import util, file_util, other_utils,nlp_util
import tika
tika.initVM()
from tika import parser
from util import sdgs_lookup 
import collections


sentences = []
sdgDic = sdgs_lookup.summary_keywords

def ConvertPdfToExcel():
    source='D:/#NLTK project/total/'
    source_list = getClassifyDoc(source)
    print ('items number:' + str(len(source_list)))
    data_list = label_list = []
    for filename in source_list:
        text = convert_pdf_to_text(source+filename+'.pdf')
        tempDataList = filterSentences(text, filename)
        tempLabelList = generateLabelList(tempDataList)
        data_list = data_list + tempDataList
        label_list = label_list + tempLabelList
    generateExcel('d:/NLPExcel','total',data_list,label_list)
    print('\n....NEUTool Finished classifying sentences.....')

def convert_pdf_to_text(pathAndFile):
    '''
    rtype: string
    Convert pdf to text
    '''
    try:
        parsedPDF = parser.from_file(pathAndFile)
        text = parsedPDF["content"]
        return text.encode('utf-8')
    except:
        pass

def filterSentences(text, filename):
    '''
    rtype:list
    Extract and filter text. 
    '''
    text = text.replace("-\n", "").replace("\n", " ")
    sent_text = nlp_util.sentenceTokenizer(text)
    data_list = []
    for i in range(len(sent_text)):
        sentence = nlp_util.remove_punctuation(sent_text[i]) # Remove punctuation
        if len(sentence) < 40:
            continue
        data_list.append(sentence.decode('utf-8'))
    return data_list
   

def generateExcel(path, doc_name, data_list,label_list):
    '''
    rtype:void
    '''
    if not os.path.isdir(path):
        other_utils.createfolder(path)
    df = pd.DataFrame(data_list)
    df['label'] = pd.Series(label_list, index=df.index)
    writer = pd.ExcelWriter(path+'/'+doc_name+'.xlsx',engine='xlsxwriter')
    df.to_excel(writer, sheet_name='sheet1',index=False,header=False)
    writer.save()

def getClassifyDoc(path):
    '''
    rtype:list
    get all the data
    '''
    classifyList = []
    for file in os.listdir(path):
        if file.endswith(".pdf"):
            classifyList.append(file[:-4])
    return classifyList


def generateLabelList(data_list):
    result = []
    for item in data_list:
        accumulateDic = collections.defaultdict(int)
        tempArray = item.split(' ')
        for word in tempArray:
            for k, v in sdgDic.iteritems():
                if word in v:
                    accumulateDic[k] += 1
                    continue
        result.append(max(accumulateDic,key=accumulateDic.get) if accumulateDic else -1)
    return result
        
     

        