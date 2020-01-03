#File to contain relevant interfaces for the bean-scraper file and the file system of the machine it runs on
import os
from xml.dom import minidom #Imports the XML parser

#Checks to see if a file exists
#Very simple for now as it just calls the os method but it might need to be expanded later hence the interface
def checkFile(filepath):
    return os.path.isfile(filepath)

#Similar to the above function but for a directory
#Implementation may need changing but works ok, will currently recognise files
def checkDir(dirpath):
    return os.path.exists(dirpath)

#Takes a line and returns any included file type url in it, that is linked to a url= tag/flag
#Very basic scraping with possibility for errors
def fileUrlScraper(rss):
    for i in range(0,len(rss)-4): #For each 4 length substring
        if ((rss[i] == 'u') & (rss[i+1] == 'r') & (rss[i+2] == 'l') & (rss[i+3] == '=')): #If its 'url='
            for j in range(i+4, len(rss)-4): #Then check each preceding 4 length substring (NOTE:-4 might be incorrect it might be -3 test this)
                if ((rss[j] == '.') & (rss[j+1] == 'm') & (rss[j+2] == 'p') & (rss[j+3] == '3')): #If its '.mp3'
                    return(rss[i+5:j+4]) #Then return it as its likely a url to an mp3 file
                elif ((rss[j] == '.') & (rss[j+1] == 'm') & (rss[j+2] == '4') & (rss[j+3] == 'a')): #If its '.m4a'
                    return(rss[i+5:j+4]) #Then return it as its likely a url to an m4a file

#Takes a full url and returns the actual filename at the end of it
#i.e https://www.dave.org/thing.pdf will return thing.pdf
def findFileName(url):
    for i in range(len(url)-1, 0, -1):
        if (url[i] == '/'):
            return (url[i+1:len(url)])


##XML STUFF

#Gets the name of a podcast from the filepath to the downloaded rss feed
#Makes the assumption the title is in element title within a channel element which is the child of the root node
#If the code does not find a title then it will return a None
def getPodcastName(filepath):
    doc = minidom.parse(filepath) #Parses the given file
    for node in doc.getElementsByTagName('channel'): #Access the channel element
        for node1 in node.getElementsByTagName('title'):
            return node1.firstChild.data


print("Starting Test")
print(getPodcastName(".rss/Qu"))
