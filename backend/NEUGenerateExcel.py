import os, sys
from src import NEUTool

def main(documents_name):
    try:
        NEUTool.ConvertPdfToExcel()
    except Exception as e:
         print e


if __name__ == '__main__':
    main(sys.argv[1])
