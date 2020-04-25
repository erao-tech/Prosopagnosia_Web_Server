# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import mysql
from flask import g

from app.sql.config.DbConfig import db_config


def connect_to_database():
    return mysql.connector.connect(user=db_config['user'], password=db_config['password'], host=db_config['host'],
                                   database=db_config['database'], use_pure=True)


def get_database():
    '''
    Description:
    These two functions allow us to connect to database and get basic information
    :return: connected database object
    '''
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

def compare_faces(target_image):
    '''
    This function compairs two faces and returns the results of the compairation if the comparation succeed, it returns True with the detected peron's name,
     if the comparation falls under special cases, the function returns False and the message
    :param target_image:
    :return:
    '''
    ##get all faces from database

    cnx = get_database()
    cursor = cnx.cursor()
    query = "SELECT cloud_image_name, person_name FROM file_info"
    cursor.execute(query)
    results = cursor.fetchall()

    # if there is no image in database:
    if len(results) == 0:
        return False, "No Reference Face in Database"

    dictList = []
    fileNumber = len(results)

    # build the dictList
    for i in range(fileNumber):
        newdict = dict()
        newdict["cloudImageName"] = results[i][0]
        newdict["personName"] = results[i][1]
        dictList.append(newdict)

    client = boto3.client('rekognition')
    all_match = []
    target_image_in_s3 = {"Bucket": "ece516-bucket", "Name": target_image, }
    for ref_face_dict in dictList:
        cur_ref_face = {"Bucket": "ece516-bucket", "Name": ref_face_dict["cloudImageName"], }
        try:
            response = client.compare_faces(SimilarityThreshold=80,
                                            SourceImage={'S3Object': cur_ref_face},
                                            TargetImage={'S3Object': target_image_in_s3})
        except Exception as ex:
            if ex.response['Error']['Code'] == "InvalidParameterException":
                return False, "There is no face detected"
            else:
                return False, str(ex)
        cur_ref_face_name = ref_face_dict["personName"]
        match_result = dict()
        match_result['name'] = cur_ref_face_name
        match_result['score'] = 0.0
        if len(response['FaceMatches']) == 0:
            continue
        for faceMatch in response['FaceMatches']:
            position = faceMatch['Face']['BoundingBox']
            similarity = str(faceMatch['Similarity'])
            print('The face at ' +
                  str(position['Left']) + ' ' +
                  str(position['Top']) +
                  ' matches with ' + similarity + '% confidence')
            if (float(similarity) >  match_result['score']):
                match_result['score'] = round(float(similarity),2)
        all_match.append(match_result)

    if len(all_match) == 0:
        return False, "Image matches none of the face in database"

    all_match = sorted(all_match, reverse=True, key=lambda match_obj: match_obj["score"])

    return True, all_match
