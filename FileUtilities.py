#File to contain relevant interfaces for the bean-scraper file and the file system of the machine it runs on
import os
from xml.dom import minidom #Imports the XML parser
from WebUtilities import downloadFile #Imports the file downloader

#Checks to see if a file exists
#Very simple for now as it just calls the os method but it might need to be expanded later hence the interface
def checkFile(filepath):
    return os.path.isfile(filepath)

#Similar to the above function but for a directory
#Implementation may need changing but works ok, will currently recognise files
def checkDir(dirpath):
    return os.path.exists(dirpath)

#Removes the given line from a file
def removeLine(lineNo, filepath):
    lines = []
    file1 = open(filepath, 'r') #Opens the file to read
    for line in file1: #Gets all lines
        lines.append(line) #Stores the lines
    file1.close()
    file1 = open(filepath, 'w') #Opens the file overwritting it
    del lines[lineNo-1]
    file1.writelines(lines)


#Takes a string and checks if there are any illegal characters for a file path
#Somewhat basic
def filePathCompliant(path):
    for char in path:
        if (char == '<'):
            print("Illegal Character '<'")
            return False
        elif (char == '>'):
            print("Illegal Character '>'")
            return False
        elif (char == ':'):
            print("Illegal Character ':'")
            return False
        elif (char == '\"'):
            print("Illegal Character '\"'")
            return False
        elif (char == '/'):
            print("Illegal Character '/'")
            return False
        elif (char == '\\'):
            print("Illegal Character '\\'")
            return False
        elif (char == '|'):
            print("Illegal Character '|'")
            return False
        elif (char == '?'):
            print("Illegal Character '?'")
            return False
        elif (char == '*'):
            print("Illegal Character '*'")
            return False
    return True

#Takes a name which would become part of a file path and removes invalid stuff
#Here we define invalid as not a-z 0-9 or select punctuation
def cleanForLinux(name):
    validChars = ""
    for char in name:
        val = ord(char)
        if ((val != 47) & (val >= 32) & (val <= 122)): #Allows all unicode characters 32 to 122 excluding 47 (forward slash)
            validChars = validChars + char
    return validChars




##XML STUFF

#Gets the name of a podcast from the url of an rss feed
#Makes the assumption the title is in element 'title' within a 'channel' element which is the child of the root node
#If the code does not find a title then it will return 'None'
def getPodcastName(url):
    downloadFile(url, ".temprss") #Downloads the rss temporarily in order to view it for its title
    doc = minidom.parse(".temprss") #Parses the downloaded file
    for node in doc.getElementsByTagName('channel'): #Access the channel element
        for node1 in node.getElementsByTagName('title'): #Accesses the title elements within the channel
            return node1.firstChild.data #Returns the first title element which should be the title of the podcast

#Given a filepath it will locate any urls within enclose tags
#This assumes that only files exist in enclose tags and that no files exist outside enclose tags
#Assumes each enclosure exists within an item along with a title element
#Returns a tuple of a title (string) and then a url
def getEnclosedLinks(filepath):
    foundUrls = [] #List to hold found pairs
    doc = minidom.parse(filepath) #Parses the given file
    for item in doc.getElementsByTagName('item'): #Runs through all items
        title = item.getElementsByTagName('title')[0].firstChild.data #Gets the title
        url = item.getElementsByTagName('enclosure')[0].getAttribute('url') #Gets the url
        title = cleanForLinux(title) #Removes any invalid characters from the title
        tup = (title, url) #Forms tuple
        foundUrls.append(tup) #Tuple added to list
    return foundUrls

#Testing
"""
print("Starting Test")
results = getEnclosedLinks(".rss/Qu")
for result in results:
    print(result[0])
    print(result[1])
"""
#removeLine(6, "testfile.txt")