#File to contain relevant interfaces for the bean-scraper file and the file system of the machine it runs on
#Checks to see if a file exists
#Very simple for now as it just calls the os method but it might need to be expanded later hence the interface
def checkFile(filepath):
    return os.path.isfile(filepath)