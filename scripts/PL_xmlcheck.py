#!/usr/bin/env python3

import xml.etree.ElementTree as ET
from sys import exit

Books = []
xmlBookList = "config/booklist.txt"
xmlBookPath = "bookfiles/"

try:
    with open(xmlBookList, 'r') as infile:
        BookList = infile.read()
        # Return a list of the lines, breaking at line boundaries.
        Books = BookList.splitlines()

except FileNotFoundError:
    print('ERROR: File open, BookList.txt not found')
    exit(1)

# Parse each xml file in channel list and process business rules
for xml in Books:
    # Parse XML using ElementTree
    try:
        book = ET.parse(xmlBookPath + xml).getroot()

    # Return error and exit if file not found
    except FileNotFoundError as e:
        print('ERROR: File open, ' + xml + ' not found: ' + str(e))
        exit(1)

    # Return error and exit if XML has syntax problems
    except SyntaxError as e:
        print('ERROR: Syntax Error in file ' + xml + ', ' + str(e))
        exit(1)

    if book.tag == 'book':
        if book.find('name') is None:
            print('ERROR: No name on book, in file ' + xml)
            exit(1)
        else:
            print('xml check is good for ' + xml)

exit(0)
