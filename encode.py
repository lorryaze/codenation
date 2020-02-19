#!/usr/bin/env python3
# importing the requests library
import requests
import json

#create a json file by a list with the response of server in json format
#the open command is a operating system command and the flag 'w' is to write in a file
#the dump command accept an object to be convert in a file
def write_json(obj):
    with open('answer.json', 'w') as f:
        json.dump(obj, f)
#open for reading
def read_json(file):
    with open('answer.json', 'r') as f:
        return json.load(f)

# api-endpoint
URL = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=cb782ac5c5013d7fa2f34906b7a68702e9a79e5b'

# sending get request and saving the response as response object dict
r = requests.get(url = URL, 
                auth=('Chickadee 75d', 
                'cb782ac5c5013d7fa2f34906b7a68702e9a79e5b')) 

#extracting data in json format 
data = r.json()

#read the data and create a json file called answer.json and put the data in this file 
write_json(data)

#print the answer.json
print(read_json('answer.json'))