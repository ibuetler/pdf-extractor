#!/usr/bin/env python3

"""
PDF Extractor for PyPDF2==3.0.1
---
Extracts the pages from a PDF file and saves them as individual PDF files.
The script will recursively search for PDF files in the given path. So if a path contains folder inside folders, they will also be scanned.

Considering the path contains following content:
.
└── exam
    ├── John_Doe
    │   └── Doe_John.pdf
    ├── Jane_Smith
    │   └── Smith_Jane.pdf
    └── Joe_Bloggs
        └── Bloggs_Joe.pdf
4 directories, 3 files

You only need to give one path, which is the path to 'exam' and not to each student individually.

Arguments:
    -p, --path: The path to the folder that contains the PDF files.
    -v, --verbose: Prints the progress of the extraction per-page.
    -h, --help: Prints the help message.

Example:
    python pdf-extractor.py -p /path/to/folder
    python pdf-extractor.py -p /path/to/folder -v

Author: Florian Kaiser (https://krypton.ninja)
"""
import argparse
import os
import PyPDF2

from PyPDF2 import PdfReader, PdfWriter


# Parse arguments of the script
parser = argparse.ArgumentParser(
    description="Recursively extracts PDF pages from a PDF file in a directory")
parser.add_argument(
    "-p", "--path", help="path to the folder that contains the PDF files", required=True)
parser.add_argument("-f", "--force", help="force the extraction of already previously extracted files", action="store_true")
parser.add_argument("-v", "--verbose",
                    help="prints the progress of the extraction per-page", action="store_true")
args = parser.parse_args()
path = args.path


def contains_number(string: str) -> bool:
    return any(char.isdigit() for char in string)


print("PDF Extractor started!\n\n")
print("PyPDF2==" + PyPDF2.__version__)

files_to_handle = []
paths_to_ignore = []
# Recursive iterator over the path to find PDF files and add them to a list of files to handle
for root, dirs, files in os.walk(path):
    for file in files:
        if contains_number(file) and not args.force:
            paths_to_ignore.append(root)
            break
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith(".pdf") and not contains_number(file) and root not in paths_to_ignore:
            data = []
            data.append(root)
            data.append(file.replace(".pdf", ""))
            files_to_handle.append(data)


# Extract the pages from the file and return a boolean on whether the extraction was successful or not
def extract(data) -> bool:
    try:
        file_root = data[0]
        file_name = data[1]

        current_file = os.path.join(file_root, f"{file_name}.pdf")
        print("current file: " + current_file)

        with open(current_file, 'rb') as f:
            pdf = PdfReader(f)
            totalPages = len(pdf.pages)

            for page in range(len(pdf.pages)):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(pdf.pages[page])
                with open(f"{os.path.join(file_root, file_name)}_{page+1}.pdf", "wb") as f:
                    if args.verbose:
                        print(f"Extracting page {page+1} of {pdf.pages} from {file_name}.pdf")
                    pdf_writer.write(f)

        return True
    except:
        raise
        return False



for item in files_to_handle:
    print(f"Extracting {item[1]}.pdf ...")
    print(f"{item[1]}.pdf extracted!") if extract(item) else print(f"{item[1]}.pdf extraction failed!")


print("\nPDF Extractor finished!")
