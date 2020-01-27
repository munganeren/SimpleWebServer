import os
from app import app
from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['xodr', 'opt.osgb', 'osgb', 'pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/xodr/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            return createResponse(False, "No file part")
        
        file = request.files['file']
        
        if file.filename == '':
            return createResponse(False, "No file selected for uploading")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(app.config['UPLOAD_FOLDER']+ '/' + filename)
            return createResponse(True, "File successfully uploaded to " + app.config['UPLOAD_FOLDER']+ '/' + filename)

        else:
            return createResponse(False, "Allowed file types are xodr, opt.osgb, osgb, pdf")

@app.route('/api/xodr/check', methods=['POST'])
def check_file():
    if request.method == 'POST':
        if 'filename' not in request.form:
            #flash('filename is not defined')
            return createResponse(False, "filename is not defined")
        
        checkFile = request.form['filename']

        if checkFile == '':
            return createResponse(False, "filename is empty")

        if os.path.isfile(app.config['UPLOAD_FOLDER']+ '/' + checkFile):
            return createResponse(True, checkFile + " is located under " + app.config['UPLOAD_FOLDER'])

        else:
            return createResponse(False, checkFile + " file does not exist.")

def createResponse(status, msg):
    return jsonify(success=status, message = msg)

if __name__ == "__main__":
    app.run()