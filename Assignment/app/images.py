from flask import render_template, redirect, url_for, session
from flask import request, send_from_directory
import os
from app import webapp
from .utils import save_file


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@webapp.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'Authenticated' not in session:
        return redirect(url_for('login'))

    if session['username']:
        username = session['username']

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return render_template('upload.html', msg='No Selected File')
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return   render_template('upload.html', msg='No Selected File')
        
        if not allowed_file(file.filename):
            return   render_template('upload.html', msg='Invalid File Type')
        
        if file and allowed_file(file.filename):
            filename = file.filename
            save_file(username, file, filename)
            return render_template('upload.html', msg='Successfully Uploaded')

    return render_template('upload.html', msg='Pleas Upload an Image')


# @webapp.route('/static/sunshine/<filename>')
# def send_image(filename):
#     return send_from_directory("images", filename)

@webapp.route('/gallery')
def gallery():
    if 'Authenticated' not in session:
        return redirect(url_for('login'))

    username = session['username']

    app_path = os.path.dirname(__file__)
    stat_path = os.path.join(app_path, 'static')
    USER_PATH = os.path.join(stat_path, username)

    image_names = os.listdir(USER_PATH)
    return render_template("gallery.html", image_names=image_names, username=username)