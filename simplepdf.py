#!/usr/bin/env python

import sys
import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter


def main():
    commands = {
        "--merge": lambda opts: merge(parse_merge_args(opts)),
        "--extract": lambda opts: extract(*parse_extract_args(opts)),
        "--rotate": lambda opts: rotate(*parse_rotate_args(opts)),
        "--insert": lambda opts: insert(*parse_insert_args(opts))
    }

    if len(sys.argv) < 2 or sys.argv[1] not in commands:
        exit_showing_help()

    command = sys.argv[1]
    opts = sys.argv[2:]
    commands[command](opts)


def exit_showing_help():
    help()
    sys.exit(1)


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


def parse_merge_args(opts):
    if len(opts) <= 1:
        exit_showing_help()
    return opts


def merge(pdfs):
    merge_file = PdfMerger()
    for pdf in pdfs[0:-1]:
        merge_file.append(PdfReader(pdf))
    merge_file.write(pdfs[-1])


def parse_extract_args(opts):
    if len(opts) != 3:
        exit_showing_help()

    input_pdf = opts[0]
    output_pdf = opts[-1]
    page_string = opts[1]
    return [input_pdf, output_pdf, page_string]


def extract(input_pdf, output_pdf, page_string):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    pages = get_pages(page_string, reader.numPages)

    for page_num in pages:
        page = reader.getPage(page_num)
        writer.addPage(page)

    writer.write(output_pdf)


def parse_rotate_args(opts):
    if len(opts) != 4:
        exit_showing_help()

    input_pdf = opts[0]
    output_pdf = opts[-1]
    page_string = opts[1]
    angle = int(opts[2])
    return [input_pdf, output_pdf, page_string, angle]


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


def parse_insert_args(opts):
    if len(opts) != 4:
        exit_showing_help()
    
    input_pdf = opts[0]
    new_pdf = opts[1]
    pos = int(opts[2])
    output_pdf = opts[3]
    return [input_pdf, new_pdf, pos, output_pdf]


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
