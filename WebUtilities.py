#File to contain relevant interfaces for the bean-scraper file and accessing the web
import urllib3
import os

#Takes a url and a filepath and downloads the file to that filepath
#Note the file path must contain the filetype, runs from root folder (i.e. location of scripts)
#Could this be done with a stream? Would that be more effective?
def downloadFile(url, filepath):
    print("Downloading --") #Start message, should contain info on what is being downloaded?
    http = urllib3.PoolManager() #Starts the PoolManager
    r = http.request('GET', url) #'gets' the file
    if (r.status == 200): #If the status is good
        file = open(filepath, 'wb') #Creates the file
        file.write(r.data) #Writes the data to the file
        file.close #Closes the file
        print("Download Complete") #Ending message
        return True
    else:
        print("Error in download, status code: " + str(r.status)) #If it fails, error code returned
        return False

#Checks to see if a file exists
def checkFile(filepath):
    return os.path.isfile(filepath)