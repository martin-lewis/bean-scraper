#Imports for the utility files, they contain an interface for dealing with the internet and file system
import FileUtilities as fileUtil
import WebUtilities as webUtil
import os

print("Starting Bean Scraper") #Test line
#webUtil.downloadFile("https://traffic.libsyn.com/secure/yogpod/Triforce_109_-_Postcode_Killah.mp3?dest-id=25170", "test3.mp3")



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

""" Test lines
print("Current feeds:")
for feed in feeds:
    print(feed)
"""

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
    #break
