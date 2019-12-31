#Imports for the utility files, they contain an interface for dealing with the internet and file system
import FileUtilities as fileUtil
import WebUtilities as webUtil

print("Starting Bean Scraper") #Test line
#webUtil.downloadFile("https://traffic.libsyn.com/secure/yogpod/Triforce_109_-_Postcode_Killah.mp3?dest-id=25170", "test3.mp3")
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
