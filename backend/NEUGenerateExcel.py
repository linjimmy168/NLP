import os, sys
from NEUTool

from src import convert_pdf_to_text, sdg_classifier, goals_summary,NEUTool

def main(documents_name):
    path='D:\\#NLTK project\\total'
    try:
        docList = NEUTool.getClassifyDoc()
        
        print 'Generate Excel Success'
    except Exception as e:
         print e


if __name__ == '__main__':
    main(sys.argv[1])
