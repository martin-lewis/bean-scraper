#Imports for the utility files, they contain an interface for dealing with the internet and file system
import FileUtilities as fileUtil
import WebUtilities as webUtil
import os
import time

##Functions

#Takes a url of a rss feed and updates the local files
def updatePodcast(rssUrl, podcastName): #Podcast name is in use for a place to put the file, the actual name is in the XML
    #Step one: Get the rss feed downloaded
    print("Downloading rss file for: " + podcastName)
    webUtil.downloadFile(rssUrl, (".rss/" + podcastName))
    #Open the file
    rss = open(".rss/" + podcastName)
    #Look through each line for an audio file
    urls =[] #List for found urls
    for line in rss: #for each line
        result = fileUtil.fileUrlScraper(line) #Check for file urls
        if (result != None): #If a result is returned then
            urls.append(result) #Added to list
    #Make sure there is a folder to hold them
    podcastFolderExists = fileUtil.checkDir(podcastName)
    if (not(podcastFolderExists)):
        os.mkdir(podcastName)
    #Downloads the files
    for url in urls:
        filename = fileUtil.findFileName(url) #Find the file name from the url
        fileAlreadyExists = fileUtil.checkFile(podcastName + "/" + filename) #Check if it has already been downloaded
        if (not(fileAlreadyExists)): #If not
            print("Fetching new file: " + filename)
            webUtil.downloadFile(url, podcastName + "/" + filename) #Download the file to the correct location
        else:
            print("file exists:" + filename) #If its already downloaded then nothing happens

##Main

print("Starting Bean Scraper") #Test line

#Start up operations before start
#Data structure and variable creation
feeds = [] #Contains the URL of each feed read from the .feeds file

#First check for the rss feeds file
feedsFileExists = fileUtil.checkFile(".feeds")
if (not(feedsFileExists)): #If there is no feeds file
    print("Creating .feeds file")
    feedsFile = open(".feeds", 'w') #Creates a new feeds file
    feedsFile.close
else: #If there is one it needs to read it
    print("Reading feeds file")
    feedsFile = open(".feeds", 'r') #Opens the feeds file
    for line in feedsFile: #Loops each line
        splitLine = line.split(',') #Splits it on commas
        feeds.append(splitLine[0]) #Gets the RSS which is in the first position of each line
    feedsFile.close()

#Rss folder
feedsFolderExists = fileUtil.checkDir(".rss")
if (not(feedsFolderExists)):
    print("Making folder")
    os.mkdir(".rss")

""" Test lines
print("Current feeds:")
for feed in feeds:
    print(feed)
"""
#Test rss download
t = updatePodcast("https://anchor.fm/s/cd90d44/podcast/rss", "Qu")

#Main program loop
while True:
    print("Welcome to Bean Scraper\nPlease select an option")
    selected = False
    while not(selected):
        print("1 - Update Podcasts\n2 - Add a Podcast\n3 - Remove a Podcast\nQ - Quit")
        response = input("Select an option\n")
        if (response == "1"):
            print("Not implimented")
            selected = True
        elif (response == "2"):
            print("Not implimented")
            selected = True
        elif (response == "3"):
            print("Not implimented")
            selected = True
        elif ((response == "Q") | (response == "q")):
            quit()
        else:
            print("Not a valid option")
            time.sleep(1)
            
    #break
