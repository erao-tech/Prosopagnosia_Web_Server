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

from app.api.HttpResponse import http_response
from flask import render_template, session, redirect, url_for

from app import webapp


@webapp.route('/')
def go_to_main_page():
    '''
    Description:

    This function runs when homepage url'/' is called, and redirect the user to login page or secured page.
    It checks if the authenticated and username information in session. If they are both in the session and the
    authenticated is true, the user will be directed to the secured page. If anything doesn't satisfy the requirements
    above, the user will then be directed to login page and authenticated and username information in session will be
    cleared.

    :return: login_index.html or secured_index.html
    '''
    # Check if illigiable to goto secured index
    if ('authenticated' in session) and ('username' in session):
        # check if the cookie includes username and authenticated flag
        if session['authenticated'] == True:
            return render_template("secured_index.html", title="MainPage", username=session['username'],
                                   membersince=session["membersince"])
        else:
            if 'username' in session:
                session.pop('username')
            if 'authenticated' in session:
                session.pop('authenticated')
            return redirect(url_for('user_login'))
    else:
        if 'username' in session:
            session.pop('username')
        if 'authenticated' in session:
            session.pop('authenticated')
        return redirect(url_for('user_login'))


@webapp.route('/upload_management')
def upload_management():
    '''
    Description:

    This function runs when upload_management page url'/upload_management' is called, and redirect user to
    upload_management page only if all session condition requirements (as mentioned in go_to_main_page) are satisfied.
    Otherwise the user will then be directed to login page and authenticated and username information in session will
    be cleared.

    :return: upload_management.html or login_index.html
    '''
    if ('authenticated' in session) and ('username' in session):
        # check if the cookie includes username and authenticated flag
        if session['authenticated'] == True:
            return render_template("upload_management.html")
    else:
        return redirect(url_for('user_login'))


@webapp.route('/process_image')
def process_image():
    '''
    Description:

    This function runs when process_image page url'/process_image' is called, and redirect user to
    process_image page only if all session condition requirements (as mentioned in go_to_main_page) are satisfied.
    Otherwise the user will then be directed to login page and authenticated and username information in session will
    be cleared.

    :return: process_image.html or login_index.html
    '''
    if ('authenticated' in session) and ('username' in session):
        # check if the cookie includes username and authenticated flag
        if session['authenticated'] == True:
            return render_template("process_image.html")
    else:
        return redirect(url_for('user_login'))


@webapp.route('/load-balancer-ping')
def ping():
    return http_response(200, "Hello World! :)")
