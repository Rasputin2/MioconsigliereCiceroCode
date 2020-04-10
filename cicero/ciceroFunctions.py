#This File Contains All the Supporting Functions for _init_.py
import os

ROOT_PATH = '/home/mioconsigliere/public_html/IRC'


#getText:
#This function takes the User Provided Code Section
#as a 'String', finds the text associated with the string
#returns the text associated with that Code provision
def getText(userInput):
    #Step One: Show the Text of the Subsection    
    import xml.etree.ElementTree as ET
    #Strip the User Input Down to The Section
    section = parse_section(userInput)
    #Find 'Section' Within User's Input 
    section = convertToXML(section)
    #Convert User's Original Input into Identifier Format for Searching XML Text
    identifier = convertToXML(userInput)
    #Determine Whether XML Node is Section, Subsection, Paragraph etc...
    xmlNode = findNode(identifier)
    if xmlNode is not None: 
        if xmlNode == 'overload':
            fullText = "Error"
        else:
            tree = ET.parse(os.path.join(ROOT_PATH, 'CodeXML.xml'))
            root = tree.getroot()
            #CAUTION: When Using Variables in the XPath, it is like PhP, You Have to Use Double Quotes "''"
            fullXMLText = root.find('.//{http://xml.house.gov/schemas/uslm/1.0}'+xmlNode+'[@identifier="'+identifier+'"]')
            fullText = (ET.tostring(fullXMLText, method='text'))
            fullText = fullText.decode('utf-8')
            #fullText = unicode(fullText,'utf-8')
    else:
        fullText = 'Error'
    #fullText Either Equals "Error" or the Text of the Section
    return fullText
    
#These functions support getText:
def cleanXMLText(string):
    returnedStr = string.replace("b","")
    returnedStr = returnedStr.replace("\n","")

def convertToXML(string):
    if string.find('(') == -1:
        returnedStr = "/us/usc/t26/s"+string
    else:
        returnedStr = string.replace(')','')
        returnedStr = returnedStr.replace('(', '/')
        returnedStr = "/us/usc/t26/s"+returnedStr 
    return returnedStr

def findNode(xPath):
    count = xPath.count("/")
    if count == 4:
        returnValue = 'section'
    elif count == 5:
        returnValue = 'subsection'
    elif count == 6:
        returnValue = 'paragraph'
    elif count == 7:
        returnValue = 'subparagraph'
    elif count == 8:
        returnValue = 'clause'
    elif count == 9:
        returnValue = 'subclause'
    elif count == 10:
        returnValue = 'item'
    elif count == 11:
        returnValue = 'subitem'
    else:
        returnValue = 'overload'
    return returnValue

#Perform Machine Learning on Code
#From Today to 1987


#Map 1986 Code to 1954 Code
#TO DO .... NEED TO FINISH THIS

#Map 1986 Code to 1939 Code
def MapTo39(string):
    #Set Default Value of Alert to 0
    alert = 0
    #Create the Dictionary
    codeMap86to39 = {}
    f = open(os.path.join(ROOT_PATH, "CurrentTo39.txt"), "r")
    if f.mode == 'r':
        for line in f:
            (key, val) = line.strip('\n').split(':')
            codeMap86to39[key] = val
    else:
        alert = 1
    f.close()
    
    #Create Recursive Function BEFORE it is Called
    def recursive86To39(argString):
        newVariable = codeMap86to39.get(argString)
        if newVariable != None:
            recursiveString = 'Code section ' + argString + ' maps to section(s) ' + newVariable + ' of the 1939 Code.'
        else:
            newString = strip_parens(argString)
            if newString == -1:
                recursiveString =  'Code section ' + argString + ' does not map to the 1939 Code.'
            else:
                recursiveString = recursive86To39(newString)
        return recursiveString
    
    #Check to Make Sure We Read File
    #If we did, Call Recursive Function to Find the Mapping
    if alert == 1:
        returnedString = 'Error: Source file could not be opened or read.'
    else:
        returnedString = recursive86To39(string)
    
    #Now Return an Error Message or the Mapping
    return returnedString

#Map 1939 to Prior Code
def Map39toPrior(string):
    #Set alert to Zero
    alert = 0
    #Create 39toPrior Dictionary
    codeMap39toPrior = {}
    f = open(os.path.join(ROOT_PATH, "1939toPrior.txt"), "r")
    if f.mode == 'r':
        for line in f:
        #The Lines in this Data File May Contain Multiple '|' Dividers
        #This First Partition Only Separates the String Based on the First Divider to Create the Key Value Pair
            strPartition = line.strip('\n').split('|')
            key = strPartition[0]
            value = strPartition[1]
            codeMap39toPrior[key] = value
    else:
        alert = 1
    f.close()
    
    #Create Recursive Function BEFORE it is Called
    def recursiveToPrior(argString):
        dictValue = codeMap39toPrior.get(argString)
        #dictValue either equals None or not None
        #if dictValue equals None, then Keep Stripping parenthesis until ...
        #there are no more parens (y = -1) or dictValue equals something
        if dictValue != None:
            dictValue = strip_percent(dictValue)
            recursiveString = 'Section ' +  argString + ' of the 1939 Code maps to the following pre-1939 Revenue Act(s) ' + dictValue + '.'
        else: 
            newString = strip_parens(argString)
            if newString == -1:
                recursiveString = 'We do not have a prior mapping for ' + argString + '.'
            else:
                recursiveString = recursiveToPrior(newString)
        return recursiveString
    
    #Check to Make Sure We Read File
    #If we did, Call Recursive Function to Find the Mapping
    if alert == 1:
        returnedString = 'Error: Source file could not be opened or read.'
    else:
        returnedString = recursiveToPrior(string)

    #Return Returned String
    return returnedString
    

#This Section Contains General Purpose Functions
#For String Manipulation
def parse_commas(string):
    if string.find(',')==-1:
        splitString = string
    else:
        splitString = string.split(',')
    return splitString

def parse_section(string):
    if string.find('(') == -1:
        returnedStr = string
    else:
        position = string.find("(")
        returnedStr = string[:position]
    return returnedStr
    
def strip_parens(string):
    if string.find('(') == -1:
        newString = -1;
    else:
        position = string.rfind('(')
        newString = string[:position]
    return newString

def strip_percent(string):
    if string.find('%')!=-1:
        strString = string.replace('%', ' and ')
    else:
        strString = string
    return strString
    
def parse_spaces(string):
    string = string.split()
    return string
