# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re
import time

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

start_time = time.time()

regex = queryToRegex('"or"[0,10]"or"[0,10]"or"')
file = open("letters/A.txt", "r") 

text = file.read() 
result = re.findall(regex, text)
resultAll = breakDown(result)

print len(resultAll)
print("--- %s seconds ---" % (time.time() - start_time))   