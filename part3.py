import time
import re
import multiprocessing
from multiprocessing import Process, Manager

start_time = time.time()
letterGroupA = ["L","W4","W2","S","Other","M","P","D","H","G","E","K","O"]
letterGroupB = ["X","Z","V","U","I","N","J","R","F","B","A","C","W3","W1","T","Y","Q"]

results = []

def queryToRegex(query):
    query = query[1:-1] # removes first and last ""
    listOfWords = query.split('"');
    regex = r""
    
    #Change query string to regex
    for i in range(0,len(listOfWords)):
        if re.search(r'\[.+?\]', listOfWords[i]) != None:     
            interval = listOfWords[i][1:-1].split(',')      
            regex += '.{' + interval[0] + ',' + interval[1] + '}'
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

def thread(letterGroup,List):
    for i in range(0,len(letterGroup)):   
        textFileName = "letters/" + letterGroup[i] + ".txt"
        file = open(textFileName, "r") 
        text  = file.read()
        result = re.findall(regex, text)
        resultAll = breakDown(result)
        List.extend(resultAll)
        file.close()       
    
def finalStats(List):
    print len(List)
    print("--- %s seconds ---" % (time.time() - start_time))
    
regex = queryToRegex('"elephants"[0,20]"are"[0,20]"to"')

if __name__ == '__main__':
    with Manager() as manager:
        List = manager.list()  # <-- can be shared between processes.
        t1 = Process(target = thread , args = (letterGroupA, List))
        t2 = Process(target = thread , args = (letterGroupB, List))
        t1.start()
        t2.start()

        t1.join()
        t2.join()
        finalStats(List)