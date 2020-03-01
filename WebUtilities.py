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
import sys

#Takes a url and a filepath and downloads the file to that filepath
#Note the file path must contain the filetype, runs from root folder (i.e. location of scripts)
#The third parameter if set to 1 will suppress the print statements in the method
def downloadFile(url, filepath, suppressed):
    try:
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
    except:
        print("\nError of type: " + str(sys.exc_info()[0]))
        return False

#Takes a URL and attempts to get the filetype from it
#Uses a HTTP GET request and the associated header 'Content-Type'
#Sets .m4a types to .mp4 which is fine as they are exactly the same for this use case
def getFileType(url):
    try:
        http = urllib3.PoolManager() #Starts the urllib3 stuff
        r = http.request('GET', url, preload_content=False) #Preload stops it downloading the file as we only want the header
        header = r.getheader("Content-Type") #Gets the part of the header that contains the file type
        info = header.split('/') #Splits the MIME into its two parts
        if (info[0] == "audio"): #If its audio
            if (info[1] == "mpeg"):
                return ".mp3" #If its mpeg then its an .mp3 file
            else:
                return "." + info[1] #Otherwise the file type is just whats given plus a .
        elif (info[0] == "video")
            if (info[1] == "mp4"):
                return ".mp4"
            elif (info[1] == "x-mp4"):
                return ".mp4"
            else:
                raise ValueError("Incompatible file type, only .mp4's are acceptable as video types at this time")
        else:
            raise ValueError("File is not a Video/Audio File") #Not currently set up to handle anything that isn't an audio file
    except:
        print("\nError of type: " + str(sys.exc_info()[0]))
        return None


#print(getFileType("https://anchor.fm/s/cd90d44/podcast/play/4309349/https%3A%2F%2Fd3ctxlq1ktw2nl.cloudfront.net%2Fstaging%2F2019-7-21%2F21427520-44100-2-7fdaeed8cbe81.m4a"))
