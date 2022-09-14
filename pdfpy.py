#!/bin/python

import sys
import os
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

OPERATIONS = ['--merge','--rotate']

def main():
    if sys.argv[1] not in OPERATIONS:
        help()
        sys.exit(1)

    if sys.argv[1] == '--merge':
        merge()

    if sys.argv[1] == '--rotate':
        rotate()

def help():
    print('pdfpy [--merge] [in1.pdf ... inN.pdf] [out.pdf]')
    print('pdfpy [--rotate] [in.pdf] [page1:-1(pageN),~page2,page7] [angle_degree (CW)] [out.pdf]')

def merge():
    if len(sys.argv) <= 3:
        help()
        sys.exit(1)

    merge_file = PdfFileMerger()
    for i in sys.argv[2:-1]:
        merge_file.append(PdfFileReader(i,'rb'))
    
    merge_file.write(sys.argv[-1])
    print(f'Merged pdfs in output pdf: {sys.argv[-1]}')

def rotate():
    if len(sys.argv) != 6:
        help()
        sys.exit(1)
    
    pdf_in = open(sys.argv[2], 'rb')
    pdf_reader = PdfFileReader(pdf_in)
    pdf_writer = PdfFileWriter()

    pages = get_pages(sys.argv[3], pdf_reader.numPages)

    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        if page_num+1 in pages:
            page.rotateClockwise(int(sys.argv[4]))
        pdf_writer.addPage(page)

    same_file = False
    if sys.argv[5] == sys.argv[2]:
        same_file = True

    if same_file:
        pdf_out = open('pdfpy_tmp'+sys.argv[5],'wb')
    else:
        pdf_out = open(sys.argv[5],'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()

    if same_file:
        os.rename('pdfpy_tmp'+sys.argv[5], sys.argv[5])


def get_pages(page_string, num_pages):
    page_array=page_string.replace('-1',str(num_pages)).replace(' ','' ).split(',')
    pages = set()

    for part in page_array:
        if ':' in part:
            pages.update(set(range(int(part.split(':')[0]),int(part.split(':')[1])+1)))
        elif '~' in part:
            if int(part.split('~')[-1]) in pages:
                pages.remove(int(part.split('~')[-1]))
        else:
            pages.add(int(part))

    return pages

if __name__=='__main__':
    main()
else:
    print('included')