#!/bin/python

import sys
import os
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

OPERATIONS = ['--merge','--rotate', '--extract']

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in OPERATIONS:
        help()
        sys.exit(1)

    if sys.argv[1] == '--merge':
        if len(sys.argv) <= 3:
            help()
            sys.exit(1)
        merge(sys.argv[2:])
    elif sys.argv[1] == '--rotate':
        if len(sys.argv) != 6:
            help()
            sys.exit(1)
        rotate(sys.argv[2], sys.argv[-1], sys.argv[3], int(sys.argv[4]))
    elif sys.argv[1] == '--extract':
        if len(sys.argv) != 5:
            help()
            sys.exit(1)
        extract(sys.argv[2], sys.argv[-1], sys.argv[3])

def help():
    print('simplepdf [--merge] [in1.pdf ... inN.pdf] [out.pdf]')
    print('simplepdf [--rotate] [in.pdf] [pages] [angle_degree (CW)] [out.pdf]')
    print('simplepdf [--extract] [in.pdf] [pages] [out.pdf] \n')
    print('Page selection: \n   1:N = from 1 to N (inclusive)\n\
    ~N = exclude page N\n\
    N = include page N\n\
    -1 = last page\n\
    Example: 1:5,~3,7,-1 will include pages 1,2,4,5,7 and the last page')

def merge(pdfs):
    merge_file = PdfFileMerger()
    for i in pdfs[0:-1]:
        merge_file.append(PdfFileReader(i,'rb'))
    merge_file.write(pdfs[-1])

def extract(input_pdf, output_pdf, page_string):
    same_file = False
    if input_pdf == output_pdf:
        same_file = True

    pdf_in = open(input_pdf, 'rb')
    pdf_reader = PdfFileReader(pdf_in)
    pdf_writer = PdfFileWriter()

    pages = get_pages(page_string, pdf_reader.numPages)

    for page_num in pages:
        page = pdf_reader.getPage(page_num)
        pdf_writer.addPage(page)

    if same_file:
        pdf_out = open('simplepdf_tmp'+output_pdf,'wb')
    else:
        pdf_out = open(output_pdf,'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()

    if same_file:
        os.rename('simplepdf_tmp'+output_pdf, output_pdf)

def rotate(input_pdf, output_pdf, page_string, angle):
    same_file = False
    if input_pdf == output_pdf:
        same_file = True
    
    pdf_in = open(input_pdf, 'rb')
    pdf_reader = PdfFileReader(pdf_in)
    pdf_writer = PdfFileWriter()

    pages = get_pages(page_string, pdf_reader.numPages)

    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        if page_num in pages:
            page.rotateClockwise(angle)
        pdf_writer.addPage(page)

    if same_file:
        pdf_out = open('simplepdf_tmp'+output_pdf,'wb')
    else:
        pdf_out = open(output_pdf,'wb')
    pdf_writer.write(pdf_out)
    pdf_out.close()
    pdf_in.close()

    if same_file:
        os.rename('simplepdf_tmp'+output_pdf, output_pdf)


def get_pages(page_string, num_pages):
    page_array=page_string.replace('-1',str(num_pages)).replace(' ','' ).split(',')
    pages = set()

    for part in page_array:
        if ':' in part:
            pages.update(set(range(int(part.split(':')[0])-1,int(part.split(':')[1]))))
        elif '~' in part:
            if int(part.split('~')[-1])-1 in pages:
                pages.remove(int(part.split('~')[-1])-1)
        else:
            pages.add(int(part)-1)

    return pages

if __name__=='__main__':
    main()
