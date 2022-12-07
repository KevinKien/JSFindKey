import os 
import re
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# Enter the website
url = input("Enter the website you want to download js file from: ")

# Make the request
r = requests.get(url)

# Get the html document structure
soup = BeautifulSoup(r.content , 'html.parser')

# Find all js files
jsfiles = soup.findall('script',type="text/javascript")

# Javascript files downloadable links 
jslinks = [js['src'] for js in jsfiles]

# Get the domain from url
host = urlparse(url).netloc

# Set the default folder for storing js files
defaultfolder = '/jsFiles'

# Create a folder for storing js files if not exist
if not os.path.exists(defaultfolder):
    os.mkdir(defaultfolder)

# Download the js files
for link in jslinks:
    # Support absoulte
    if link.startswith('http'):
        fileurl = link
    # Support relative
    else:
        fileurl = "http://"+host + link
    filename = defaultfolder+"/"+os.path.basename(fileurl)
    dicts = {'filename':filename , 'fileurl':fileurl}
    # Download the file
    with open(filename,'wb') as jsfile:
        response = requests.get(dicts['fileurl'])
        jsfile.write(response.content)

# Search for access key and secret key in the js files
for jsfile in os.listdir(defaultfolder):
    if jsfile.endswith('.js'):
        with open(defaultfolder+'/'+jsfile,'r') as jsfile:
            textdata = jsfile.read()
        # find access key
        accesskeypattern = re.findall(r'ACCESSKEY\s*=\s*\"(.+)\"',textdata)
        if accesskeypattern:
            print ("Access key in the file {} is".format(jsfile),accesskeypattern0)
        # find secret key
        secretkeypattern = re.findall(r'SECRETKEY\s*=\s*\"(.+)\"',textdata)
        if secretkeypattern:
            print ("Secret key in the file {} is".format(jsfile),secretkeypattern0)
