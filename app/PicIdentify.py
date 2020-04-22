import base64
from flask import request

from app import webapp
from app.S3Helper import store_file
from app.util.AWSHelper import compare_faces


@webapp.route('/whichface-api', methods=['POST'])
def which_face_api():
    try:
        if request.method == 'POST':
            img_file = request.form['img']

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
                    if match_result == "":
                        # connect to database and create the record
                        cnx = get_database()
                        cursor = cnx.cursor()

                        # rename the upload img as: userpid_useruploadcounter_imagename.extention
                        userFileName = secure_filename(file.filename)  # example: example.jpg
                        cloudSaveFilename = str(session["uid"]) + "_" + str(time.time()).replace('.',
                                                                                                 '') + "_" + userFileName  # example: 12_1_example.jpg

                        store_file(cloudSaveFilename, file)
                        new_file = get_file_path_by_key(cloudSaveFilename)

                        # prepare for values for sql
                        fileName = userFileName
                        uploadImagePath = UPLOAD_FOLDER + cloudSaveFilename
                        ts = time.time()
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

                        personName = str(time.time()).replace('.', '')

                        # update file_name table
                        query = "INSERT INTO file_info (file_name, upload_image_path, cloud_image_name, create_time, person_name) VALUES (%s, %s, %s, %s, %s)"
                        data = (fileName, uploadImagePath, cloudSaveFilename, timeStamp, personName)
                        cursor.execute(query, data)
                        cnx.commit()
                    return info_msg
                else:
                    result = (match_output[0]['name'], str(match_output[0]['score']))
                    return str(result)  # '200'#(match_output[0]['name'], match_output[0]['score'])

            else:
                raise Exception("Not a Correct File Type!")
    except Exception as ex:
        info_msg = "problem is:", str(ex)
        print(info_msg)
        return info_msg
