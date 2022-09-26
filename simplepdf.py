#!/usr/bin/env python

import sys
import os
import argparse
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

PAGE_STRING_HELP = """
    page selection, separated by commas:
        1:N = from 1 to N (inclusive);
        ~N = exclude page N;
        N = include page N;
        -1 = last page;
        Example: 1:5,~3,7,-1 will include pages 1,2,4,5,7 and the last page
"""

def main():
    parser = argparse.ArgumentParser(description='Simple program for manipulating pdfs')

    subparsers = parser.add_subparsers(dest='subparser_name')

    parser_merge = subparsers.add_parser('merge', help='Merge pdfs into one')
    parser_merge.add_argument('input_pdfs', nargs='*', help='List of pdf files to merge')
    parser_merge.add_argument('output_pdf', help='Merged pdf file name')
    parser_merge.set_defaults(func=merge)

    parser_extract = subparsers.add_parser('extract', help='Extract pages from pdf')
    parser_extract.add_argument('input_pdf', help='pdf to be extracted')
    parser_extract.add_argument('page_string', help=PAGE_STRING_HELP)
    parser_extract.add_argument('output_pdf', help='Extracted pdf file name')
    parser_extract.set_defaults(func=extract)

    parser_rotate = subparsers.add_parser('rotate', help='Rotate given pages of a pdf with a given angle')
    parser_rotate.add_argument('input_pdf', help='pdf to be rotated')
    parser_rotate.add_argument('page_string', help=PAGE_STRING_HELP)
    parser_rotate.add_argument('angle', type=int, help='Angle to rotate clockwise in degrees')
    parser_rotate.add_argument('output_pdf', help='Rotated pdf file name')
    parser_rotate.set_defaults(func=rotate)

    parser_insert = subparsers.add_parser('insert', help='Insert a pdf inside another pdf at a given position')
    parser_insert.add_argument('input_pdf', help='Base pdf file')
    parser_insert.add_argument('inserted_pdf', help='pdf to be inserted into input_pdf')
    parser_insert.add_argument('position', type=int, help='Page where the pdf should be inserted')
    parser_insert.add_argument('output_pdf', help='Final pdf file name')
    parser_insert.set_defaults(func=insert)

    args = parser.parse_args()
    args.func(args)


def merge(args):
    merge_file = PdfMerger()
    for pdf in args.input_pdfs:
        merge_file.append(PdfReader(pdf))
    merge_file.write(args.output_pdf)


def extract(args):
    reader = PdfReader(args.input_pdf)
    writer = PdfWriter()

    pages = get_pages(args.page_string, reader.numPages)

    for page_num in pages:
        page = reader.getPage(page_num)
        writer.addPage(page)

    writer.write(args.output_pdf)


def rotate(args):
    reader = PdfReader(args.input_pdf)
    writer = PdfWriter()

    pages = get_pages(args.page_string, reader.numPages)

    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        if page_num in pages:
            page.rotateClockwise(args.angle)
        writer.addPage(page)

    writer.write(args.output_pdf)


def get_pages(page_string, num_pages):
    page_array = page_string.replace("-1", str(num_pages)).replace(" ", "").split(",")
    pages = set()

    for part in page_array:
        if ":" in part:
            pages.update(
                set(range(int(part.split(":")[0]) - 1, int(part.split(":")[1])))
            )
        elif "~" in part:
            if int(part.split("~")[-1]) - 1 in pages:
                pages.remove(int(part.split("~")[-1]) - 1)
        else:
            pages.add(int(part) - 1)

    return pages


def insert(args):
    base_reader = PdfReader(args.input_pdf)
    inserted_reader = PdfReader(args.inserted_pdf)
    writer = PdfWriter()

    page_num = 0
    while page_num < args.position - 1:
        page = base_reader.getPage(page_num)
        writer.addPage(page)
        page_num += 1

    for page in inserted_reader.pages:
        writer.addPage(page)

    while page_num < base_reader.numPages:
        page = base_reader.getPage(page_num)
        writer.addPage(page)
        page_num += 1

    writer.write(args.output_pdf)


if __name__ == "__main__":
    main()
