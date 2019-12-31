#File to contain relevant interfaces for the bean-scraper file and the file system of the machine it runs on
import os

#Checks to see if a file exists
#Very simple for now as it just calls the os method but it might need to be expanded later hence the interface
def checkFile(filepath):
    return os.path.isfile(filepath)

#Similar to the above function but for a directory
#Implementation may need changing but works ok, will currently recognise files
def checkDir(dirpath):
    return os.path.exists(dirpath)