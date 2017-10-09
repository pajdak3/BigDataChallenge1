# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re

urlname = '{http://www.mediawiki.org/xml/export-0.10/}'
file = open('letters/A.txt','a') # Opens and appends to the file

def cleanText(text):
    text = text.replace('\n', ' ') # Replaces new line with white space
    text = re.sub(r'\s\s+', r' ', text) # Changes big white spaces to single white space
    text = text.lower() # Lowercase
    text = text.encode('utf-8').strip() # Encodes the text to utf-8 format
    return text

def loadxmlfile(data):
    filename = ET.iterparse(data)

    firstLetter = ''
    
    #Go through one element at a time, so we don't fill the memory
    for event, element in filename:
        # Element is a whole element
        if element.tag == (urlname + 'title'):
            if element.text != None:
                firstLetter = re.search(r'[a-üA-Ü]+', element.text) #Finds the first alphabet/word in the title
        if element.tag == (urlname + 'text'):
            if element.text != None:
                if firstLetter:
                    if firstLetter.group()[0] == 'A' or firstLetter.group()[0] == 'a':
                        text = cleanText(element.text)
                        file.write(text)
        #Important to clear the element from the memory, so we don't fill it
        element.clear()


loadedText = loadxmlfile('enwiki.xml')  

file.close()