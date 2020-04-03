import base64
import io
import json
import urllib

from flask import Flask, request
import requests
from app import webapp
from app.util.AWSHelper import compare_faces


@webapp.route('/')
def hello_world():
    return "ECE516"


@webapp.route('/whichface',methods=['POST'])
def which_face():
    img_file = request.files['img']
    img_bytes = img_file.read()
    face_matches = compare_faces(img_bytes)
    return str(face_matches)

