import xml.etree.ElementTree
from xml.dom import minidom
from lxml import etree
from sys import exit


def strip(elem):    # Function to strip whitespace and newlines from elements.
    for elem in elem.iter():
        if elem.text:
            elem.text = elem.text.strip()
        if elem.tail:
            elem.tail = elem.tail.strip()

xmlBookList = "C:\\Users\\stuar\\Books\\config\\booklist.txt"
xmlBookPath = "C:\\Users\\stuar\\Books\\bookfiles\\"
xml_schema = "C:\\Users\\stuar\\Books\\config\\bookschema.xsd"

# define Objects
# ElementTree Obj for combined XML
combET = xml.etree.ElementTree
# ElementTree Obj for individual channel XML
indET = xml.etree.ElementTree

# Set XML root tag in combined file
root = combET.Element('books')
# Get root tree
tree = combET.ElementTree(root)

# Get channel list
BookList = []
try:
    with open(xmlBookList, 'r') as infile:
        BookList = infile.read()

except FileNotFoundError as e:
    print('ERROR:[File Open Error]: Error in opening channel list, ' + str(e))
    exit(1)

# Return a list of the lines, breaking at line boundaries.
InChannels = BookList.splitlines()

targetChannelCount = len(InChannels)
actualChannelCount = 0

try:
    for xml in InChannels:
        channel = indET.parse(xmlBookPath + xml).getroot()
        root.append(channel)
        actualChannelCount += 1

except FileNotFoundError as e:
    print('ERROR:[File Open Error]: Error in opening XML file, ' + str(e))
    exit(1)

strip(root)     # Remove whitespace
output = combET.tostring(root)
# print(output)

# Pretty print format of xml file
outfile = minidom.parseString(combET.tostring(root)).toprettyxml(indent='\t')

print(outfile)

print('INFO:[LCM Merge]: Merge completed')
print('INFO:[LCM Merge]: ' + str(actualChannelCount) + ' Channels processed and merged from target of '
      + str(targetChannelCount))

'''# Write pretty to file
with open("Outfile.xml", "w") as f:
    f.write(outfile)'''


# Merged XML check with schema
LCMSchema = None
try:
    with open(xml_schema, 'rb') as schema_file:
        LCMSchema = schema_file.read()

except FileNotFoundError as e:
    print('ERROR:[File Open Error]: Error opening XML Schema file, ' + str(e))
    exit(1)

# parse xml
try:
    doc = etree.XML(outfile)
    print('INFO:[LCM Check]: LCM XML syntax OK.')

# check for file IO error
except IOError:
    print('Invalid File')

# check for XML syntax errors
except etree.XMLSyntaxError as e:
    print('ERROR: [XML Syntax Error]: ' + str(e))
    exit(1)

# validate against schema
try:
    xmlschemaDoc = etree.XML(LCMSchema)
    xmlschema = etree.XMLSchema(xmlschemaDoc)
    xmlDoc = etree.XML(outfile)
    xmlschema.assertValid(xmlDoc)
    print('INFO:[LCM Check]: Schema validation OK.')

except etree.DocumentInvalid as e:
    print('Error:[Schema Validation] : ' + str(e))
    exit(1)

exit(0)
