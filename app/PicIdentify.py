import base64
import datetime
import time
from flask import request, session
from werkzeug.utils import secure_filename

from app import webapp
from app.FileUploader import get_database, UPLOAD_FOLDER
from app.S3Helper import store_file, get_file_path_by_key
from app.util.AWSHelper import compare_faces

request_list = []

@webapp.route('/whichface-api', methods=['POST'])
def which_face_api():
    '''
    This function is called by the Vuzix Blade, the return from this functioin will be pure string
    :return:
    '''
    global request_list
    try:
        if request.method == 'POST':
            img_file = request.form['img']

            request_id = request.form['requestId']

            if request_id in request_list:
                return "Duplicated request"
            else:
                request_list.append(request_id)

            img_file = base64.b64decode(img_file)

            if img_file:
                # ===================================================#
                # ======Till this step the file is good to process===#
                # ===================================================#
                # img_bytes = img_file.read()
                store_file('temp_image.jpg', img_file)
                match_result, match_output = compare_faces('temp_image.jpg')
                if match_result == False:
                    info_msg = match_output
                    print(match_output)
                    if match_output == "There is no face detected":
                        request_list.remove(request_id)
                        return "There is no face detected"
                    if match_output == "Image matches none of the face in database":
                        # connect to database and create the record
                        cnx = get_database()
                        cursor = cnx.cursor()

                        # rename the upload img as: userpid_useruploadcounter_imagename.extention

                        cloudSaveFilename = "vuzix" + "_" + str(time.time()).replace('.',
                                                                                                 '')  # example: 12_1_example.jpg

                        store_file(cloudSaveFilename, img_file)


                        # prepare for values for sql
                        fileName = cloudSaveFilename
                        uploadImagePath = UPLOAD_FOLDER + cloudSaveFilename
                        ts = time.time()
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                        personName = "reference_face_" + str(time.time()).replace('.', '')

                        # update file_name table
                        query = "INSERT INTO file_info (file_name, upload_image_path, cloud_image_name, create_time, person_name) VALUES (%s, %s, %s, %s, %s)"
                        data = (fileName, uploadImagePath, cloudSaveFilename, timeStamp, personName)
                        cursor.execute(query, data)
                        cnx.commit()
                        request_list.remove(request_id)
                    request_list.remove(request_id)
                    return "A NEW FACE added as No." + personName[15:] + " please add name tag later through web app"
                else:
                    request_list.remove(request_id)
                    result = (match_output[0]['name'], str(match_output[0]['score']))
                    return str(result)  # '200'#(match_output[0]['name'], match_output[0]['score'])
            else:
                request_list.remove(request_id)
                raise Exception("Not a Correct File Type!")

    except Exception as ex:
        info_msg = "problem is:", str(ex)
        print(info_msg)
        return info_msg
