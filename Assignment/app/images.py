from flask import render_template, redirect, url_for, session
from flask import request, send_from_directory
import os
from app import webapp
from .utils import save_file, validator
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# limit the uploaded files' types.
def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#upload webpage
@webapp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'Authenticated' not in session:
        return redirect(url_for('login'))

    if session['username']:
        username = session['username']
    else:
        return redirect(url_for('login'))

    if request.method == 'POST':
        # check if the post request has the file part
        if 'files' not in request.files:
            return render_template('upload.html', msg='No Selected File')

        #file = request.files['file']
        files = request.files.getlist('files')

        # if user does not select file, browser also
        # submit an empty part without filename
        for file in files:
            if file.filename == '':
                return   render_template('upload.html', msg='No Selected File')

            if len(file.filename) > 50:
                return   render_template('upload.html', msg='Filename is Too Long!')

            if not allowed_file(file.filename):
                return   render_template('upload.html', msg='Invalid File Type')

            if request.content_length > 5 * 1024 * 1024:
                return render_template('upload.html', msg='Files are Too Big!')

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_file(username, file, filename)
        return render_template('upload.html', msg='Successfully Uploaded')

    return render_template('upload.html', msg='Pleas Upload an Image')

#gallery webpage
@webapp.route('/gallery', methods=['GET'])
def gallery():
    if 'Authenticated' not in session:
        return redirect(url_for('login'))

    username = session['username']

    app_path = os.path.dirname(__file__)
    stat_path = os.path.join(app_path, 'static')
    USER_PATH = os.path.join(stat_path, username)
    # ORIGIN_PATH = os.path.join(USER_PATH, 'origin')
    # OCR_PATH = os.path.join(USER_PATH,'ocr')
    THUMB_PATH = os.path.join(USER_PATH,'thumbnails')

    # origin_names = os.listdir(ORIGIN_PATH)
    # ocr_names = os.listdir(OCR_PATH)
    thumb_names = os.listdir(THUMB_PATH)

    return render_template("gallery.html", image_names=thumb_names, username=username)

#detail page for a specific image. each page contain 2 images: one for ocr and the other for org.
@webapp.route('/detail/<image_name>', methods=['GET'])
def detail(image_name):
    if 'Authenticated' not in session:
        return redirect(url_for('login'))

    username = session['username']
    return render_template("detail.html", username=username, image_name=image_name)


#for easy testing, api/upload page.
@webapp.route('/api/upload', methods=['GET'])
def script_upload():
    return render_template('api_upload.html')

@webapp.route('/api/upload', methods=['POST'])
def api_upload():
    msg = 'Pleas Upload an Image'
    username = request.form['username']
    password = request.form['password']
    if validator(username,password) is not None:
        msg = 'Invalid Username/Password'
        return render_template('api_upload.html', msg=msg)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            msg = 'No Selected File'
            return render_template('api_upload.html', msg=msg)

        #file = request.files['file']
        files = request.files.getlist('file')

        # if user does not select file, browser also
        # submit an empty part without filename
        for file in files:
            if file.filename == '':
                msg = 'No Selected File'
                return   render_template('api_upload.html', msg=msg)

            if not allowed_file(file.filename):
                msg = 'Invalid File Type'
                return   render_template('api_upload.html', msg=msg)

            if request.content_length > 5 * 1024 * 1024:
                msg = 'Files are Too Big!'
                return render_template('api_upload.html', msg=msg)

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_file(username, file, filename)
        msg = 'Successfully Uploaded'

        session.pop('Authenticated', None)
        session.pop('id', None)
        session.pop('username', None)

        return render_template('api_upload.html', msg=msg)

    return render_template('api_upload.html', msg=msg)


