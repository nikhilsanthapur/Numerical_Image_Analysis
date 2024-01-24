import os
from app import app
from flask import Flask, flash, request, jsonify
from werkzeug.utils import secure_filename

# setting up folder name
folder_name = 'image_server'

# setting up app config properties
app.config['UPLOAD_FOLDER'] = folder_name

extensions = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

def checkFileExtensions(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensions

@app.route('/api/images/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        response_error = jsonify({'status': False,
                       'message': 'Image not found in request'})
        response_error.status_code = 400
        return response_error

    files = request.files.getlist('image')
    errors = {}
    success_message = False
    for photo in files:
		
        if photo and checkFileExtensions(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(app.config['UPLOAD_FOLDER'],photo.category+filename))
            success_message = True
        else:
            errors[photo.filename] = 'Image type is not allowed'
    if success_message and errors:
        errors['message'] = jsonify({'data': photo.filename,
                                    'status': True,
                                    'message': 'Image(s) successfully uploaded'
                                    })
        resp = jsonify(errors)
        resp.status_code = 500
        return resp

if __name__ == '__main__':
    app.run(host="127.0.0.1",port=5000,debug=True)
