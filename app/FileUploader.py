import datetime
import time

import mysql.connector
from flask import request, redirect, url_for, send_from_directory, render_template, session, g
from werkzeug.utils import secure_filename

from app import webapp
from app.S3Helper import store_file, get_file_path_by_key, create_presigned_url_expanded, delete_file
from app.sql.config.DbConfig import db_config
# The function used to establish connection to sql database
from app.util.AWSHelper import compare_faces


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


# UPLOAD_FOLDER = '/home/ubuntu/ece1779_projects/img/'

# UPLOAD_FOLDER = '/Users/fredpan/Desktop/output/'

# UPLOAD_FOLDER = '/home/yixiao/Desktop/after/'

UPLOAD_FOLDER = '/'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
webapp.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    '''
    Description:
    This function checks allowed extension type.
    :param filename: The file name which need to be judged
    :return: True if the file is illegible and False if its not
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# after user click the upload button
@webapp.route('/name_tag_modify', methods=['POST'])
def name_tag_modify():
    name_tag = request.form.get('nameTag', "")
    imageName = request.form.get('imageName', "")
    # update database
    # connect to database and create the record
    cnx = get_database()
    cursor = cnx.cursor()
    sql = "UPDATE file_info SET person_name = %s WHERE cloud_image_name = %s"
    val = (name_tag, imageName)
    cursor.execute(sql, val)
    cnx.commit()
    session['info'] = "Name Tag Updated!"
    return redirect(url_for('file_management'))


# after user click the upload button
@webapp.route('/delete_image', methods=['POST'])
def delete_image():
    deleteImageName = request.form.get('deleteImageName', "")
    # delete image from s3
    resut1 = delete_file(deleteImageName)
    # delete image from database
    resut2 = True
    try:
        cnx = get_database()
        cursor = cnx.cursor()
        sql = "DELETE FROM file_info WHERE cloud_image_name = %s"
        val = (deleteImageName,)
        cursor.execute(sql, val)
        cnx.commit()
    except Exception as ex:
        resut2 = False

    if not (resut1 and resut2):
        session['error'] = "A problem occurred while deleting file!"
    else:
        session['info'] = "File deleted!"
    return redirect(url_for('file_management'))


# after user click the upload button
@webapp.route('/which_face', methods=['POST'])
def which_face():
    try:
        if request.method == 'POST':
            img_file = request.files['img']

            # check if the post request has the file part
            if 'img' not in request.files:
                raise Exception("No file upload in the request!")

            # test if file too large:

            # if user does not select file, browser also

            # submit an empty part without filename
            if img_file.filename == '':
                raise Exception("No file selected!")
            if len(img_file.filename) >= 50:
                raise Exception("File name too long")

            if img_file and allowed_file(img_file.filename):

                # ===================================================#
                # ======Till this step the file is good to process===#
                # ===================================================#

                # img_bytes = img_file.read()
                store_file('temp_image.jpg', img_file)
                match_result, match_output = compare_faces('temp_image.jpg')
                temp_image_path = create_presigned_url_expanded('temp_image.jpg')
                error_msg = None
                info_msg = None
                if match_result == False:
                    info_msg = match_output
                    return render_template("process_image.html", uploadImagePath=temp_image_path,
                                           match_result=str(match_output), info_msg=info_msg, error_msg=error_msg)
                else:
                    info_msg = "Match succeed, result as follows:"
                    return render_template("process_image.html", uploadImagePath=temp_image_path,
                                           match_result=str(match_output), info_msg=info_msg, error_msg=error_msg)

            else:
                raise Exception("Not a Correct File Type!")
    except Exception as ex:
        print("problem is:", str(ex))
        return render_template("process_image.html", error_msg=str(ex))


# after user click the upload button
@webapp.route('/upload', methods=['POST'])
def upload_file():
    '''
    Description:

    This function will be called if the user tries to upload an image and this function checks if the upload is valid.
    If so the function will keep a copy of the image and an OpenCV-processed image in the database, with the proper
    naming scheme.
    The function can raise exceptions if there are any of the following problems: no file selected; filename too long;
    wrong extension type; file too large.
    If the uploaded is valid then we will connect to the database and create a record. First, we update the information
    in session from our database. Second, we assign systematic names to the image and its processed image depending on
    the user id and their upload counter. Third, we save the image to the cloud, process it through OpenCV and then
    save the processed image to the cloud. Fourth, we gather all information and update our file name table in the
    database. Last we increase the upload counter by 1 and update it.
    :return: upload_management.html
    '''

    try:
        if request.method == 'POST':
            file = request.files['file']
            # check if the post request has the file part
            if 'file' not in request.files:
                raise Exception("No file upload in the request!")

            # test if file too large:

            # if user does not select file, browser also

            # submit an empty part without filename
            if file.filename == '':
                raise Exception("No file selected!")
            if len(file.filename) >= 50:
                raise Exception("File name too long")

            if file and allowed_file(file.filename):

                # ===================================================#
                # ======Till this step the file is good to process===#
                # ===================================================#

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
                input_name = request.form.get('nameTag', "")
                if input_name.strip() != '':
                    personName = input_name

                # update file_name table
                query = "INSERT INTO file_info (file_name, upload_image_path, cloud_image_name, create_time, person_name) VALUES (%s, %s, %s, %s, %s)"
                data = (fileName, uploadImagePath, cloudSaveFilename, timeStamp, personName)
                cursor.execute(query, data)
                cnx.commit()

                # get the image path for both image_before and image_after
                info_msg = "Photo  Uploaded Successfully!"

                return render_template("upload_management.html",
                                       uploadImagePath=create_presigned_url_expanded(cloudSaveFilename),
                                       fileName=fileName, person_name=personName, info_msg=info_msg)

            else:
                raise Exception("Not a Correct File Type!")
    except Exception as ex:
        print("problem is:", str(ex))
        return render_template("upload_management.html", error_msg=str(ex))


@webapp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(webapp.config['UPLOAD_FOLDER'], filename)


@webapp.route('/file_management')
def file_management():
    '''
    This function allows user to check uploaded and processed images when the url'/file_management' is called.
    If the session information is all valid, we will connect to the database and try to get all images with the
    required uid and then show them.
    :return: "file_management.html"
    '''
    if ('authenticated' in session) and ('username' in session):
        # check if the cookie includes username and authenticated flag
        if session['authenticated'] == True:
            # ==========prepare the loop for flexable amont of images===========#
            # connect to database and create the record
            cnx = get_database()
            cursor = cnx.cursor()
            query = "SELECT file_name, cloud_image_name, person_name FROM file_info"
            cursor.execute(query)
            results = cursor.fetchall()

            # if there is no uploaded image:
            if len(results) == 0:
                return render_template("file_management.html", fileNumber=0, dictList=[])

            # if there exists uploaded image:
            else:
                # need following args for render html template : dictList, filenumber>0
                # for each dictionary in dictList, 5 elements:
                # modelName: ex. model1
                # cloudSaveFilename: ex. 07_2_example.jpg
                # cloudProcessedFileName ex. p_07_2_example.jpg
                # userFileName: ex. example.jpg
                # processedUserFileName: ex. processed_example.jpg

                dictList = []
                fileNumber = len(results)

                # build the dictList
                for i in range(fileNumber):
                    newdict = dict()
                    newdict["userFileName"] = results[i][0]
                    newdict["cloudSaveFilename"] = create_presigned_url_expanded(results[i][1])
                    newdict["cloudImageName"] = results[i][1]
                    newdict["personName"] = results[i][2]
                    newdict["modalID"] = "modal" + str(i)
                    newdict["buttonID"] = "button" + str(i)
                    newdict["closeID"] = "close" + str(i)

                    dictList.append(newdict)

                info_msg = None
                if ('info' in session):
                    info_msg = session['info']
                    session.pop('info')

                error_msg = None
                if ('error' in session):
                    error_msg = session['error']
                    session.pop('error')

                return render_template("file_management.html", fileNumber=fileNumber, dictList=dictList,
                                       info_msg=info_msg, error_msg=error_msg)

    else:
        return redirect(url_for('user_login'))
