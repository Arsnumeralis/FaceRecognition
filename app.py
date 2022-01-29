from flask import Flask, request
import os
from flask.wrappers import Response
from vector_collection import vector_collection, average_representation
from recognition import recognising
import numpy
import cv2
import re

uploads = r"ref"
allowed_extentions = {
    "jpg", "png", "jpeg"
}

app = Flask(__name__)
app.config["ref"] = uploads

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in allowed_extentions

@app.route("/")
def Homepage():
    return {
        "Route to machine learning upload": "/ref-upload",
        "Route to recognition upload": "/rec-upload"
    }

@app.route("/ref-upload", methods=["POST"])
def ref_upload():
    files = request.files.getlist("file_name")
    name = request.form["person_name"]
    if not os.path.isdir(os.path.join(app.config["ref"], name)):
        os.mkdir(os.path.join(app.config["ref"], name))
    uploaded = []
    for file in files:
        if allowed_file(file.filename):
            # as opposed to saving the image, it is represented as an rgb array
            imgstr = file.read()
            npimg = numpy.fromstring(imgstr, numpy.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            vector_collection(name, file.filename, img)
            uploaded.append(file.filename)
    average_representation(name)
    return {"message": f"uploaded {uploaded}"}


@app.route("/rec-upload", methods=["POST"])
def rec_upload():
    file = request.files["file_name"]
    if allowed_file(file.filename):
        try:
            # as opposed to saving the image, it is represented as an rgb array
            imgstr = file.read()
            npimg = numpy.fromstring(imgstr, numpy.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            for name in os.listdir("ref"):
                if recognising(os.path.join("ref", name), img) == True:
                    name_parts = [part.capitalize() for part in name.split("_")]
                    converted_name = " ".join(name_parts)
                    return {"message": f"Person found! It's {converted_name}."}
            return {"message": "No matching person found on database."}
        except:
            return {"message": "The picture either contains no face or too many."}
                
    else:
        return {"message": "File format not supported. Please uploade .png, .jpg or .jpeg files."}


if __name__ == "__main__":
    app.run(debug=True)