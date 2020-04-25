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

# Data Base Configuration

'''
This file includes a dictionary named db_config which has 4 keys: user, password, host and database which contains the
information of database IP address, default login database, database login username and password, all values in Strings.
'''

db_config = {'user': 'admin',
             'password': 'password',
             'host': 'ece516database.crfeccmcbvji.us-east-1.rds.amazonaws.com',
             'database': 'ece516'}
