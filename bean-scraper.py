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
        result = webUtil.fileUrlScraper(line) #Check for file urls
        if (result != None): #If a result is returned then
            urls.append(result) #Added to list
    #Make sure there is a folder to hold them
    podcastFolderExists = fileUtil.checkDir(podcastName)
    if (not(podcastFolderExists)):
        os.mkdir(podcastName)
    #Downloads the files
    for url in urls:
        filename = webUtil.findFileName(url) #Find the file name from the url
        fileAlreadyExists = fileUtil.checkFile(podcastName + "/" + filename) #Check if it has already been downloaded
        if (not(fileAlreadyExists)): #If not
            print("Fetching new file: " + filename)
            webUtil.downloadFile(url, podcastName + "/" + filename) #Download the file to the correct location
        else:
            print("file exists:" + filename) #If its already downloaded then nothing happens

#Takes the url of a podcast and updates the local files
def updatePodcastXML(url):
    #First get the podcasts name
    name = fileUtil.getPodcastName(url) #Gets the name from the url
    name = fileUtil.cleanForLinux(name) #Removes any characters from a name that are invalid in linux
    if (name == None): #Checks if it has found no name
        print("Error - Podcast has no name...") #If so this is an error
        return
    #Downloading the rss file
    print("Downloading rss file for: " + name)
    webUtil.downloadFile(url, (".rss/" + name)) #Downloads the rss file
    urls = fileUtil.getEnclosedLinks(".rss/" + name) #Gets the enclosed links and titles from the file
    #Check for a folder
    podcastFolderExists = fileUtil.checkDir(name)
    if (not(podcastFolderExists)):
        os.mkdir(name)
    #Run the urls
    for url in urls:
        fileAlreadyExists = fileUtil.checkFile(name + "/" + url[0]) #Checks to see if the file is already downloaded
        if (not(fileAlreadyExists)): #If not
            print("Fetching new file: " + url[0])
            webUtil.downloadFile(url[1], name + "/" + url[0]) #Download the file to the correct location
        else:
            print("file exists:" + url[0]) #If its already downloaded then nothing happens

##Functions for running the menu

#Takes a url and adds it to the .feeds
#Just adds the given string to the file along with the name of the podcast
def addPodcast(url):
    name = fileUtil.getPodcastName(url) #Gets the name of the podcast
    name = fileUtil.cleanForLinux(name) #Removes invalid characters
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



##Main

print("Starting Bean Scraper") #Welcome Line

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
feedsFolderExists = fileUtil.checkDir(".rss") #Checks if the folder exists
if (not(feedsFolderExists)): #If not creates it
    print("Making folder")
    os.mkdir(".rss")


#Main program loop
while True:
    print("Welcome to Bean Scraper\nPlease select an option")
    selected = False
    while not(selected):
        print("1 - Update Podcasts\n2 - Add a Podcast\n3 - Remove a Podcast\n4 - Show current Podcasts\nQ - Quit")
        response = input("Select an option\n")
        if (response == "1"):
            print("Not implemented")
            selected = True
        elif (response == "2"): #Add Podcast
            feedToAdd = input("Enter the URL of the RSS feed\n")
            ##TODO: Some validation? See issue #6
            addPodcast(feedToAdd)
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
        elif (response == "4"): #Show Podcasts
            names = getPodcasts() #Gets the list of podcasts
            if (len(names) == 0):
                print("No podcasts") #If theres no podcasts
            else:
                print("\nCurrent Podcasts are:") #Prints podcasts
                for i in range(0,len(names)):
                    print(str(i+1) + " - " + names[i])
                print("\n")
            selected = True
            time.sleep(1)
        elif ((response == "Q") | (response == "q")):
            quit() #Quites
        else: #Catch all for the rest
            print("Not a valid option")
            time.sleep(1)
            
    #break
