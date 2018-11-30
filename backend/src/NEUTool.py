# -*- coding: utf-8 -*-
import os, sys
import pandas as pd
sys.path.append(os.path.join(os.path.dirname(__file__)))
from utils import util, file_util, other_utils,nlp_util
import tika
tika.initVM()
from tika import parser

sentences = []

# Extracts sentences from text file and labels all the SDG mentioned in each sentence
def ConvertPdfToExcel():
    source='D:/#NLTK project/total/'
    source_list = getClassifyDoc()
    print ('items number:' + str(len(source_list)))
    for filename in source_list:
        text = convert_pdf_to_text(source+filename+'.pdf')
        filterSentences(text, filename) # Returns labelled sentences for given text file
    print('\n....NEUTool Finished classifying sentences.....')

def convert_pdf_to_text(pathAndFile):
    print pathAndFile
    try:
        parsedPDF = parser.from_file(pathAndFile)
        text = parsedPDF["content"]
        return text.encode('utf-8')
    except:
        pass

def filterSentences(text, filename):
    text = text.replace("-\n", "").replace("\n", " ")
    sent_text = nlp_util.sentenceTokenizer(text)
    data_list = []
    for i in range(len(sent_text)):
        
        sentence = nlp_util.remove_punctuation(sent_text[i]) # Remove punctuation
        if len(sentence) < 40:
            continue
        data_list.append(sentence.decode('utf-8'))
    generateExcel('d:/NLPExcel',filename[:-4],data_list)
    

def generateExcel(path, doc_name, data_list):
    if not os.path.isdir(path):
        other_utils.createfolder(path)

    df = pd.DataFrame(data_list)
    writer = pd.ExcelWriter(path+'/'+doc_name+'.xlsx',engine='xlsxwriter')
    df.to_excel(writer, sheet_name='sheet1',index=False)
    writer.save()

def getClassifyDoc():
    '''
    rtype:list
    get the classify document name
    '''
    clasifyStr = 'Cook_Islands_7_11	Egypt_10-10	Kosovo_23_11    Kiribati_4.10	Kenya_12-10	Kyrgyzstan_20.10	Ethiopia_4.10	Gambia_4.10	Rwanda_10_10	Philippines_10_10	Samoa_10_10	Saint_Vincent_and_the_Grenadines_2_11	Liberia_25_10	Mexico_7_11	Marshall-Islands_4.10_arrows-edited	Moldova_4.10	Micronesia_10_11	Myanmar_14-10	Mozambique_10-10	Mongolia_10_10	Nauru_10_10	Nepal_25_10	Nigeria_1_11	Pakistan_25_10	Niue_31_10	Palau_2_11	Papa_New_Guinea_14-10	Belarus_4.10	Bangladesh_4.10	Armenia_12_10	Angola_10-10	Albania_21_10	Afghanistan_16_11	Zimbabwe_14-10	Yemen_25_10	Viet_Nam_14-10	Vanuatu_10_10	Uganda_7_11	Tuvalu_10_10	Tonga_10_10	Timor-Leste_31_10	Tanzania_4.10	Tajikistan_14-10	Somalia_31_10	Solomon_Islands_10_10	10632NationalVoluntaryReviewReport(rev_final)	10647estonia	16005Azerbaijan    Fiji_12_10	Lao_25_10	Malawi_10_10	Bhutan_24_10	10611Finland_VNR	10617FullReportHLPF2016_Switzerland_ENfin	10686HLPF-Bericht_final_EN	10689UgandaReviewReport_CDs1	10695Montenegro-HLPFReport	10720sierraleone	10726ReportSDGsFrance	107102030AgendaTurkeyReport	WDR_2006Equityanddevelopment	WDR_2009_bookweb_1	WDR_2012Genderequalityanddevelopment	WDR_2013_Report	Pakistan_25_10	Solomon_Islands_10_10'
    classifyList = []
    newStr = ''
    for i,v in enumerate(clasifyStr):
        if i > 0 and (clasifyStr[i-1].isalnum or clasifyStr[i-1].isalnum) and v.isspace() and len(newStr) > 0:
            classifyList.append(newStr)
            newStr = ''
        if v.isspace():
            continue
        newStr += v
    classifyList.append(newStr)
    return classifyList