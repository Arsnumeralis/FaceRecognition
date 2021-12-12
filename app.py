from flask import Flask, request, render_template, session
import os
from flask.wrappers import Response

uploads = r"C:\Users\pmick\Desktop\Python\face"
allowed_extentions = {
    "jpg", "png", "jpeg", "xml"
}

app = Flask(__name__)
app.config["uploads"] = uploads

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
    if not os.path.isdir(os.path.join(app.config["uploads"], "machine-learning", name)):
        os.mkdir(os.path.join(app.config["uploads"], "machine-learning", name))
    uploaded = []
    for file in files:
        if allowed_file(file.filename):
            upload_file = file.filename
            uploaded.append(upload_file)
            file.save(os.path.join(app.config["uploads"], "machine-learning", name, upload_file))
            print(uploaded)
    return {"uploaded": uploaded}


@app.route("/rec-upload", methods=["POST"])
def rec_upload():
    file = request.files["file_name"]
    if allowed_file(file.filename):
        file.save(os.path.join(app.config["uploads"], "recognition", file.filename))
        return {"uploaded": file.filename}
    else:
        return {"message": "file format not supported"}


if __name__ == "__main__":
    app.run(debug=True)