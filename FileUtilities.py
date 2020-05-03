"""
    Bean Scraper - File Utilities
    Copyright (C) 2019-2020  Martin Lewis

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

#File to contain relevant interfaces for the bean-scraper file and the file system of the machine it runs on
import os
from xml.dom import minidom #Imports the XML parser
from WebUtilities import downloadFileStream #Imports the file downloader
import sys

#Checks to see if a file exists
#Very simple for now as it just calls the os method but it might need to be expanded later hence the interface
def checkFile(filepath):
    return os.path.isfile(str(filepath))

#Similar to the above function but for a directory
#Implementation may need changing but works ok, will currently recognise files
def checkDir(dirpath):
    return os.path.exists(str(dirpath))

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

#Takes a name which would become part of a file path and removes invalid stuff
#Here we define invalid as not a-z 0-9 or select punctuation
def cleanForLinux(name):
    validChars = ""
    for char in name:
        val = ord(char)
        if ((val != 47) & (val >= 32) & (val <= 122)): #Allows all unicode characters 32 to 122 excluding 47 (forward slash)
            validChars = validChars + char
    return validChars

#Takes a name and removes all the characters that windows will not want to deal with
#Mostly replaces them with spaces
def cleanForWindows(name):
    validChars = ""
    for char in name:
        val = ord(char)
        if (val == 33):
            validChars = validChars + " " #Replaces ! with a Space
        elif (val == 34):
            validChars = validChars + " " #Replaces " with a Space
        elif (val == 42):
            validChars = validChars + " " #Replaces * with a Space
        elif (val == 47):
            validChars = validChars + " " #Replaces / with a Space
        elif (val == 58):
            validChars = validChars + " " #Replaces : with a Space (Replace with ;)
        elif (val == 60):
            validChars = validChars + " " #Replaces < with a Space
        elif (val == 62):
            validChars = validChars + " " #Replaces > with a Space
        elif (val == 63):
            validChars = validChars + " " #Replaces ? with a Space
        elif (val == 92):
            validChars = validChars + " " #Replaces \ with a Space
        elif (val == 124):
            validChars = validChars + " " #Replaces | with a Space
        elif ((val >= 32) & (val <= 122)): #Allows all unicode characters 32 to 122
            validChars = validChars + char
        else:
            validChars = validChars + " " #Anything else is replaced with a space
    
    #Removes any spaces or .s that are on the end of a file name
    while ((validChars[len(validChars) -1] == ' ') | (validChars[len(validChars) -1] == '.')):
        validChars = validChars[:len(validChars)-1]

    #Removes any double spaces
    i = 0
    while (i < len(validChars)-1): #While needed as the len(validChars) changes as things are removed
        #print(i)
        if ((validChars[i] == ' ') & (validChars[i+1] == ' ')): #If there is a space next to another space
            validChars = validChars[:i+1] + validChars[i+2:] #Remove one space
        else:
            i = i +1 #Otherwise we move to the next space

    return validChars




##XML STUFF

#Gets the name of a podcast from the url of an rss feed
#Makes the assumption the title is in element 'title' within a 'channel' element which is the child of the root node
#If the code does not find a title then it will return 'None'
def getPodcastName(url):
    success = downloadFileStream(url, ".temprss", 1) #Downloads the rss temporarily in order to view it for its title
    if (success == None):
        return None
    try:
        doc = minidom.parse(".temprss") #Parses the downloaded file
        for node in doc.getElementsByTagName('channel'): #Access the channel element
            for node1 in node.getElementsByTagName('title'): #Accesses the title elements within the channel
                return node1.firstChild.data #Returns the first title element which should be the title of the podcast
    except:
        print("\nError of type: " + str(sys.exc_info()[0]))
        return None

#Given a filepath it will locate any urls within enclose tags
#This assumes that only files exist in enclose tags and that no files exist outside enclose tags
#Assumes each enclosure exists within an item along with a title element
#Returns a tuple of a title (string) and then a url
def getEnclosedLinks(filepath):
    foundUrls = [] #List to hold found pairs
    doc = minidom.parse(filepath) #Parses the given file
    for item in doc.getElementsByTagName('item'): #Runs through all items
        try:
            title = item.getElementsByTagName('title')[0].firstChild.data #Gets the title
            try:
                url = item.getElementsByTagName('enclosure')[0].getAttribute('url') #Gets the url
                title = cleanForWindows(title) #Removes any invalid characters from the title
                tup = (title, url) #Forms tuple
                foundUrls.append(tup) #Tuple added to list
            except IndexError: #Catches errors
                print("Index Error")
        except IndexError:
            print("Index Error")

    return foundUrls

#Testing
#print(cleanForWindows("Triforce! #108:  in Mama Mia") + "|")