#!/usr/bin/python3.7
import requests
url = 'http://54.161.20.123:5000/whichface'
# url = 'http://localhost:5000/whichface'
imageSource = open('C:\\Users\\felix\\Desktop\\Steve-Mann-Jasleen-Arneja-940x627.jpg', 'rb')
img = {'img': imageSource,'img2':imageSource}
response = requests.post(url, files=img)
print(response.content)