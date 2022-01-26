from flask import Flask, request
import os
from flask.wrappers import Response
from vector_collection import vector_collection
from recognition import recognising
import numpy
import cv2
import re

uploads = r"ml"
allowed_extentions = {
    "jpg", "png", "jpeg"
}

app = Flask(__name__)
app.config["ml"] = uploads

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit(".", 1)[1].lower() in allowed_extentions

@app.route("/")
def Homepage():
    return {
        "Route to machine learning upload": "/ml-upload",
        "Route to recognition upload": "/rec-upload"
    }

@app.route("/ml-upload", methods=["POST"])
def ml_upload():
    files = request.files.getlist("file_name")
    name = request.form["person_name"]
    if not os.path.isdir(os.path.join(app.config["ml"], name)):
        os.mkdir(os.path.join(app.config["ml"], name))
    uploaded = []
    for file in files:
        if allowed_file(file.filename):
            imgstr = file.read()
            npimg = numpy.fromstring(imgstr, numpy.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            vector_collection(name, file.filename, img)
            uploaded.append(file.filename)
    return {"message": f"uploaded {uploaded}"}


@app.route("/rec-upload", methods=["POST"])
def rec_upload():
    file = request.files["file_name"]
    if allowed_file(file.filename):
        try:
            imgstr = file.read()
            npimg = numpy.fromstring(imgstr, numpy.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            for name in os.listdir("ml"):
                if recognising(os.path.join("ml", name), img) == True:
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