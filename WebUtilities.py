"""
    Bean Scraper - Web Utilities
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
#File to contain relevant interfaces for the bean-scraper file and accessing the web
import urllib3
import os

#Takes a url and a filepath and downloads the file to that filepath
#Note the file path must contain the filetype, runs from root folder (i.e. location of scripts)
#The third parameter if set to 1 will suppress the print statements in the method
def downloadFile(url, filepath, suppressed):
    if (suppressed != 1):
        print("Downloading --") #Start message, should contain info on what is being downloaded?
    http = urllib3.PoolManager() #Starts the PoolManager
    r = http.request('GET', url) #'gets' the file
    if (r.status == 200): #If the status is good
        file = open(filepath, 'wb') #Creates the file
        file.write(r.data) #Writes the data to the file
        file.close #Closes the file
        if (suppressed != 1) :
            print("Download Complete") #Ending message
        return True
    else:
        print("Error in download, status code: " + str(r.status)) #If it fails, error code returned
        return False

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