# FaceRecognition

This is a facial recognition webapp. Currently it can only successfully identify a person if the image only contains one face facing the camera with some leeway.

Dependencies are listed in the requirements.txt file.

The following files will be needed to run the app:

1. dlib_face_recognition_resnet_model_v1.dat (link - http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2)
2. mmod_human_face_detector.dat (link - http://dlib.net/files/mmod_human_face_detector.dat.bz2)
3. shape_predictor_5_face_landmarks.dat (link - http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2)

To run, type "flask run" in the command line while in the directory containing the app.py file. 

Optional arguments are "--host" and "--port".

The app has two api endpoints - one for uploading reference material and the other for face recognition:

# Reference upload:
Type "/ml-upload" at the end of the address when calling the api.

In the body tab select form with file upload enabled.

Form field name has to contain "person_name" and the value is the name of the person in snake case, e.g. "elton_john"

You can upload multiple files to this endpoint. The field name must contain "file_name" for the file to be processed.

If the upload is successful the response will be an object containing a list of uploaded file names.

# Recognition upload:
Type "/rec-upload" at the end of the address when calling the api.

This endpoint only accepts one file to be uploaded per call.

The field name must be named "file_name". 

Upon success, the response will either name the person detected, confirm there isn't such person in the database, or claim that the picture contains either no face or too many faces depending on what's in the uploaded picture.

# Accepted file formats:
.png .jpg .jpeg
