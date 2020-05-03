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
#The third parameter if set to 1 will suppress the print statements, that are not as a result of errors, in the method
def downloadFile(url, filepath, suppressed):
    try:
        if (suppressed != 1):
            print("Downloading --") #Start message
        http = urllib3.PoolManager() #Starts the PoolManager
        r = http.request('GET', url) #'gets' the file
        if (r.status == 200): #If the status is good
            file1 = open(filepath, 'wb') #Creates the file
            file1.write(r.data) #Writes the data to the file
            file1.close #Closes the file
            r.release_conn()
            if (suppressed != 1) :
                print("Download Complete") #Ending message
            return True
        else:
            print("Error in download, status code: " + str(r.status)) #If it fails, error code returned
            return False
    except:
        print("\nError of type: " + str(sys.exc_info()[0]))
        return False

#Takes a url and a filepath and downloads the file to that filepath
#Note the file path must contain the filetype, runs from root folder (i.e. location of scripts)
#The third parameter if set to 1 will suppress the print statements, that are not as a result of errors, in the method
#This method uses a streamed version which means it downloads it in small chunks, having a smaller affect on the memory
def downloadFileStream(url, filepath, suppressed):
    try:
        if (suppressed != 1):
            print("Downloading --") #Start message
        http = urllib3.PoolManager() #Starts the PoolManager
        r = http.request('GET', url, preload_content=False) #Gets the file but does not start downloading it
        if (r.status == 200): #If the status is good
            file1 = open(filepath, 'wb') #Creates the file
            for chunk in r.stream(): #Now downloads the file in chunks of 2**16 bytes (default)
                file1.write(chunk) #Writes the current data
            file1.close #Closes the file
            r.release_conn() #Releases the connection as all the data has been downloaded
            if (suppressed != 1) :
                print("Download Complete") #Ending message
            return True
        else:
            print("Error in download, status code: " + str(r.status)) #If it fails, error code returned
            return False
    except:
        print("\nError of type: " + str(sys.exc_info()[0])) #Catch all for other errors
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
        elif (info[0] == "video"):
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
