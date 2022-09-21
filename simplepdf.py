#!/usr/bin/env python

import sys
import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter

OPERATIONS = ["--merge", "--rotate", "--extract", "--insert"]


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in OPERATIONS:
        help()
        sys.exit(1)

    if sys.argv[1] == "--merge":
        if len(sys.argv) <= 3:
            help()
            sys.exit(1)
        merge(sys.argv[2:])
    elif sys.argv[1] == "--rotate":
        if len(sys.argv) != 6:
            help()
            sys.exit(1)
        rotate(sys.argv[2], sys.argv[-1], sys.argv[3], int(sys.argv[4]))
    elif sys.argv[1] == "--extract":
        if len(sys.argv) != 5:
            help()
            sys.exit(1)
        extract(sys.argv[2], sys.argv[-1], sys.argv[3])
    elif sys.argv[1] == "--insert":
        if len(sys.argv) != 6:
            help()
            sys.exit(1)
        insert(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5])


def help():
    print("simplepdf [--merge] [in1.pdf ... inN.pdf] [out.pdf]")
    print("simplepdf [--rotate] [in.pdf] [pages] [angle_degree (CW)] [out.pdf]")
    print("simplepdf [--extract] [in.pdf] [pages] [out.pdf]")
    print("simplepdf [--insert] [in.pdf] [add.pdf] [page] [out.pdf]\n")
    print(
        "Page selection: \n   1:N = from 1 to N (inclusive)\n\
    ~N = exclude page N\n\
    N = include page N\n\
    -1 = last page\n\
    Example: 1:5,~3,7,-1 will include pages 1,2,4,5,7 and the last page"
    )


def merge(pdfs):
    merge_file = PdfMerger()
    for pdf in pdfs[0:-1]:
        merge_file.append(PdfReader(pdf))
    merge_file.write(pdfs[-1])


def extract(input_pdf, output_pdf, page_string):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    pages = get_pages(page_string, reader.numPages)

    for page_num in pages:
        page = reader.getPage(page_num)
        writer.addPage(page)

    writer.write(output_pdf)


def rotate(input_pdf, output_pdf, page_string, angle):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    pages = get_pages(page_string, reader.numPages)

    for page_num in range(reader.numPages):
        page = reader.getPage(page_num)
        if page_num in pages:
            page.rotateClockwise(angle)
        writer.addPage(page)

    writer.write(output_pdf)


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


def insert(input_pdf, new_pdf, pos, output_pdf):
    reader = PdfReader(input_pdf)
    reader2 = PdfReader(new_pdf)
    writer = PdfWriter()

    page_num = 0
    while page_num < pos - 1:
        page = reader.getPage(page_num)
        writer.addPage(page)
        page_num += 1

    for page in reader2.pages:
        writer.addPage(page)

    while page_num < reader.numPages:
        page = reader.getPage(page_num)
        writer.addPage(page)
        page_num += 1

    writer.write(output_pdf)


if __name__ == "__main__":
    main()
