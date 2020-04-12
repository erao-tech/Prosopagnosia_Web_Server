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
