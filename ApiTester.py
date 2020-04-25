#!/usr/bin/python3.7

#  Copyright 2020 EraO Prosopagnosia Helper Dev Team, Liren Pan, Yixiao Hong, Hongzheng Xu, Stephen Huang, Tiancong Wang
#
#  Supervised by Prof. Steve Mann (http://www.eecg.toronto.edu/~mann/)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import requests

'''
This is a tester for testing the API
'''

url = 'http://127.0.0.1:5000/whichface'
imageSource = open('/home/yixiao/Desktop/Steve-Mann-Jasleen-Arneja.jpg', 'rb')
img = {'img': imageSource}
response = requests.post(url, files=img)
print(response.content)