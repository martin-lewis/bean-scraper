#Imports for the utility files, they contain an interface for dealing with the internet and file system
import FileUtilities as fileUtil
import WebUtilities as webUtil

print("Starting Bean Scraper") #Test line
webUtil.downloadFile("https://traffic.libsyn.com/secure/yogpod/Triforce_109_-_Postcode_Killah.mp3?dest-id=25170", "test3.mp3")