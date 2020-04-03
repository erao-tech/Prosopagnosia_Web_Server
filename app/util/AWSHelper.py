# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# PDX-License-Identifier: MIT-0 (For details, see https://github.com/awsdocs/amazon-rekognition-developer-guide/blob/master/LICENSE-SAMPLECODE.)

import boto3
import requests

def get__all_reference_faces():
    s3 = boto3.resource('s3')
    my_bucket = s3.Bucket('ece516-bucket')
    all_reference_faces = []
    for file in my_bucket.objects.filter(Prefix="reference_faces/"):
        if (file.key != "reference_faces/"):
            all_reference_faces.append(file.key)
    return all_reference_faces



def compare_faces(target_image_bytes):
    allRefFaces = get__all_reference_faces()
    client = boto3.client('rekognition')
    all_match = []

    for ref_face in allRefFaces:
        cur_ref_face = {"Bucket": "ece516-bucket","Name": ref_face,}
        response = client.compare_faces(SimilarityThreshold=80,
                                        SourceImage={'S3Object': cur_ref_face},
                                        TargetImage={'Bytes': target_image_bytes})
        cur_ref_face_name = ref_face[16:-4]
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

    all_match = sorted(all_match, reverse=True, key=lambda match_obj: match_obj["score"])
    return all_match[0]

