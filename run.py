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

from app import webapp

'''
This file is the main program which has to be run to start the website service. The program imports the “app” class 
in the same directly which includes all the website framework and resources of our website. The program start the 
webserver with host set to 0.0.0.0 which mean the server listen to all the IP address.
'''
webapp.run(host='0.0.0.0',debug=True)
