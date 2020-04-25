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

import boto3 as boto3
from botocore.exceptions import ClientError
from flask import logging


def delete_file(file_name):
    try:
        s3 = boto3.resource("s3")
        obj = s3.Object("ece516-bucket", file_name)
        obj.delete()
    except Exception as ex:
        return False
    return True


def store_file(file_name, file):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # Upload the file
    s3_client = boto3.resource('s3')
    try:
        response = s3_client.Bucket("ece516-bucket").put_object(Key=file_name, Body=file)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def get_file_path_by_key(key):
    s3_client = boto3.client('s3')
    response = s3_client.get_object(Bucket="ece516-bucket", Key=key)
    return response['Body'].read()


def create_presigned_url_expanded(objName):
    """Generate a presigned URL to invoke an S3.Client method

    Not all the client methods provided in the AWS Python SDK are supported.

    :param client_method_name: Name of the S3.Client method, e.g., 'list_buckets'
    :param method_parameters: Dictionary of parameters to send to the method
    :param expiration: Time in seconds for the presigned URL to remain valid
    :param http_method: HTTP method to use (GET, etc.)
    :return: Presigned URL as string. If error, returns None.
    """

    # Generate a presigned URL for the S3 client method
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={
                                                        'Bucket': 'ece516-bucket',
                                                        'Key': objName,
                                                    },
                                                    ExpiresIn=30)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response
