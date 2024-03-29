"""
    Bean Scraper - Main file
    Copyright (C) 2019-2023  Martin Lewis

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

#Imports for the utility files, they contain an interface for dealing with the internet and file system
import sys
sys.dont_write_bytecode = True #Prevents the __pycahce__ folder being created, that folder only confuses the folder structure
import FileUtilities as fileUtil
import WebUtilities as webUtil
import os
import time
from pathlib import Path

##Functions

#Takes the url of a podcast and updates the local files
def updatePodcastXML(url):
    #First get the podcasts name
    name = fileUtil.getPodcastName(url) #Gets the name from the url
    if (name == None): #Checks if it has found no name
        print("Error - Podcast has no name...") #If so this is an error
        return
    name = fileUtil.cleanForWindows(name) #Removes any characters from a name that are invalid in linux
    #Downloading the rss file
    rssFilepath = Path(".rss/" + name)
    print("\nDownloading rss file for: " + name)
    success = webUtil.downloadFileStream(url, rssFilepath, 0) #Downloads the rss file
    if (success == False):
        print("Error in updating podcast")
        return
    else:
        print("Checking for new episodes")
    urls = fileUtil.getEnclosedLinks(str(rssFilepath)) #Gets the enclosed links and titles from the file
    #Check for a folder
    podcastFolderExists = fileUtil.checkDir(name)
    if (not(podcastFolderExists)):
        os.mkdir(name)
    #Run the urls (episodes)
    for url in urls:
        filePathSansType = Path(name + "/" + url[0]) #Generates the filepath for where the new file will go
        fileAlreadyExists = fileUtil.checkFileSansType(filePathSansType) #Checks to see if the file is already downloaded
        if (not(fileAlreadyExists)): #If not
            filetype = webUtil.getFileType(url[1]) #Gets the filetype of the file the url points to
            if (filetype == None): #If the filetypes is not found correctly
                print("Error Downloading file") #Error message
                continue #Try next file
            filePath = Path(name + "/" + url[0] + filetype) #Create the filepath where the file will be downloaded to
            print("Fetching new file: " + url[0])
            success = webUtil.downloadFileStream(url[1], filePath, 0) #Download the file to the correct location
            if (success == None):
                print("Error - File not downloaded")
        #else:
            #print("file exists:" + url[0]) #If its already downloaded then nothing happens

##Functions for running the menu

#Takes a url and adds it to the .feeds
#Just adds the given string to the file along with the name of the podcast
def addPodcast(url):
    name = fileUtil.getPodcastName(url) #Gets the name of the podcast
    if (name == None): #Checks if it has found no name
        print("Error - There has been an issue getting the podcasts name...\n") #If so this is an error
        return
    name = fileUtil.cleanForWindows(name) #Removes invalid characters
    file = open(".feeds", 'a')
    file.writelines(url + "," + name + "\n")
    file.close

#Takes a validated number and then must remove the number th line of .feeds
def removePodcast(number):
    fileUtil.removeLine(number, ".feeds")
    return
    
#Returns a list of names from the .feeds file
def getPodcasts():
    file = open(".feeds", 'r') #opens file to read it
    names = [] #Gets a list for the names
    for line in file: #Runs through the lines
        splitLine = line.split(',') #Splits on the ,
        names.append(splitLine[1]) #Gets the name, the second item in the line
    file.close #Closes the file
    return names

#Rechecks the .feeds file and returns the list of urls
#This is in case the feeds are updated by removal or addition of new podcasts
def updateFeeds():
    newFeed = []
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
            newFeed.append(splitLine[0]) #Gets the RSS which is in the first position of each line
        feedsFile.close()
    
    return newFeed

def interactive():
    while True:
        print("Please select an option")
        selected = False
        while not(selected):
            print("1 - Update Podcasts\n2 - Add a Podcast\n3 - Remove a Podcast\n4 - Show current Podcasts\nQ - Quit")
            response = input("Select an option\n")
            if (response == "1"):
                for feed in feeds:
                    updatePodcastXML(feed)
                selected = True
                print("\nUpdates Complete\n")
            elif (response == "2"): #Add Podcast
                feedToAdd = input("Enter the URL of the RSS feed\n")
                ##TODO: Some validation? See issue #6
                addPodcast(feedToAdd)
                feeds = updateFeeds()
                selected = True
            elif (response == "3"): #Remove Podcast
                #TODO: Print All podcasts
                names = getPodcasts()
                if (len(names) == 0): #If there are no podcasts then none can be removed
                    print("No podcasts")
                    time.sleep(1)
                    selected = True
                else: #If there are podcasts
                    print("Current Podcasts are:")
                    for i in range(0,len(names)):
                        print(str(i+1) + " - " + names[i]) #Prints current podcasts
                    toRemove = input("Select which podcast to remove\n") #Take a value representing which to remove
                    try:
                        val = int(toRemove)
                        if ((val > 0) & (val <= len(names))):
                            removePodcast(val)
                            selected = True

                        else:
                            print("Not a valid number")
                            time.sleep(1)
                    except ValueError:
                        #Handle the exception
                        print("Not a number")
                        time.sleep(1)
                feeds = updateFeeds()
            elif (response == "4"): #Show Podcasts
                names = getPodcasts() #Gets the list of podcasts
                if (len(names) == 0):
                    print("No podcasts") #If there's no podcasts
                else:
                    print("\nCurrent Podcasts are:") #Prints podcasts
                    for i in range(0,len(names)):
                        print(str(i+1) + " - " + names[i])
                    print("\n")
                selected = True
                time.sleep(1)
            elif ((response == "Q") | (response == "q")):
                quit() #Quits
            elif ((response == "W") | (response == "w")): #Warranty Information
                print(
                    """
        GPL-3.0

        15. Disclaimer of Warranty.

        THERE IS NO WARRANTY FOR THE PROGRAM, TO THE EXTENT PERMITTED BY
        APPLICABLE LAW.  EXCEPT WHEN OTHERWISE STATED IN WRITING THE COPYRIGHT
        HOLDERS AND/OR OTHER PARTIES PROVIDE THE PROGRAM "AS IS" WITHOUT WARRANTY
        OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO,
        THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
        PURPOSE.  THE ENTIRE RISK AS TO THE QUALITY AND PERFORMANCE OF THE PROGRAM
        IS WITH YOU.  SHOULD THE PROGRAM PROVE DEFECTIVE, YOU ASSUME THE COST OF
        ALL NECESSARY SERVICING, REPAIR OR CORRECTION.

                    """
                )
                time.sleep(1)
            elif ((response == "C") | (response == "c")): #Copyright Information
                print("\nPlease see the relevant section of the GPL-3.0 which should be contained with this file")
                print("Otherwise it can be found at https://www.gnu.org/licenses/gpl-3.0.html\n")
                time.sleep(1)
            else: #Catch all for the rest
                print("Not a valid option")
                time.sleep(1)

##Main
#Licence Notice
print("Bean Scraper  Copyright (C) 2019-2020  Martin Lewis\nThis program comes with ABSOLUTELY NO WARRANTY; for details type \'w\'")
print("This is free software, and you are welcome to redistribute it under certain conditions; type \'c\' for details.\n")


time.sleep(1)
print("Starting Bean Scraper") #Welcome Line

#Start up operations before start
#Data structure and variable creation
feeds = updateFeeds()

#Rss folder
feedsFolderExists = fileUtil.checkDir(".rss") #Checks if the folder exists
if (not(feedsFolderExists)): #If not creates it
    print("Making folder")
    os.mkdir(".rss")

if (len(sys.argv) > 1):
    if (sys.argv[1] == "-u"):
        for feed in feeds:
            updatePodcastXML(feed)
else:
    interactive()