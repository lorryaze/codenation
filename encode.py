#!/usr/bin/env python3
# importing the requests library
import requests
import json
import hashlib

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

#Decoded message function
def decode(str, number):
    i = 0
    arr = []
    for s in str:
        aux = ord(s)
        if(aux >= 97  and aux <= 122):
            pos = aux - 97
            pos -= number
            if(pos < 0):
                pos += 26
            sub = 97 + pos
            arr.append(chr(sub))
        else:
            sub = aux
            arr.append(chr(sub))
        i += 1
    decoded = ''.join(arr)
    #print(decoded)
    return decoded
#Econded message function
#def encoded(str):

# api-endpoint
URL = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=cb782ac5c5013d7fa2f34906b7a68702e9a79e5b'

# sending get request and saving the response as response object dict
r = requests.get(url = URL, 
                auth=('Chickadee 75d', 
                'cb782ac5c5013d7fa2f34906b7a68702e9a79e5b')) 

#extracting data in json format 
data = r.json()
number = data['numero_casas']
encrypted = data['cifrado']

#call the decoded message function
decoded = decode(encrypted, number)

#Enconding decoded message
encoding = hashlib.sha1(decoded.encode()).hexdigest()

#inserting the decoded message int the data dict
data['decifrado'] = decoded
data['resumo_criptografico'] = encoding

#read the data(dict) and create a json file called answer.json and put the data in this file 
write_json(data)

#Response
#files={'answer': open('answer.json', 'r')}
URL_RESPONSE = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=cb782ac5c5013d7fa2f34906b7a68702e9a79e5b'
response = requests.post(url = URL_RESPONSE, files={'answer': open('answer.json', 'r')})
print(response.status_code)

#print the answer.json
#print("Response status: ", r)
#print("Response in dict form: ", data)
print("Answer file: ", read_json('answer.json'))
#print("Number of 'numero_casas': ", number)
#print("Encrypted message: ", encrypted)
print("Decoded message: ", decoded)
print("Encoded message: ", encoding)
