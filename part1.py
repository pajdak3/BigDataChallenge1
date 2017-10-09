# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re

def cleanText(text):
    text = text.replace('\n', ' ') # Replaces new line with white space
    text = re.sub(r'\s\s+', r' ', text) # Changes big white spaces to single white space
    text = text.lower() # Lowercase
    text = text.encode('utf-8').strip() # Encodes the text to utf-8 format
    return text

def queryToRegex(query):
    query = query[1:-1] # removes first and last ""
    listOfWords = query.split('"') # Splits string by “
    regex = r""
    
    #Change query string to regex “cat[0,10]hat” = cat.{0.10}hat
    for i in range(0,len(listOfWords)):
        #Checks if this string parts is in [0,10] format
        if re.search(r'\[.+?\]', listOfWords[i]) != None:     
            interval = listOfWords[i][1:-1].split(',')      
            regex += '.{' + interval[0] + ',' + interval[1] + '}' #.{0,10}
        else:
            regex += listOfWords[i]
   
    return regex

def breakDown(array): 

    for i in range(0,len(array)): 
        textLeft = array[i][1:]
        textRight = array[i][0:-1]

        left = re.findall(regex, textLeft)
        right = re.findall(regex, textRight)
        if right:
            array.extend(breakDown(right))
        if left:
            array.extend(breakDown(left))
    return array

#Load the xml file
def loadxmlfile(train):
    filename = ET.parse(train)
    root = filename.getroot()
    
    text = root.find('parse').find('text').text
    
    return text
   
loadedText = loadxmlfile('cats.xml')

beatifyText = cleanText(loadedText) 
regex = queryToRegex('"english"[0,200]"cat"')

result = re.findall(regex, beatifyText)
print len(result)
resultAll = breakDown(result)

print resultAll
print len(resultAll)