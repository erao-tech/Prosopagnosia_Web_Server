#!/usr/bin/python3.7
import requests

'''
This is a tester for testing the API
'''

url = 'http://127.0.0.1:5000/whichface'
imageSource = open('/home/yixiao/Desktop/Steve-Mann-Jasleen-Arneja.jpg', 'rb')
img = {'img': imageSource}
response = requests.post(url, files=img)
print(response.content)