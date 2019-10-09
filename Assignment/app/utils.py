import hashlib, uuid
from .database import connect_to_database,  get_db, teardown_db
import os
import  app.ocr.text_detection as text_detection
from .ocr.thumbnails import thumbnails

#hashfunction
def hashed_password(word, salt):
    password = hashlib.sha512(word.encode('utf-8') + salt.encode('utf-8')).hexdigest()
    return password

#save username and password to database
def save_reg(username,password):
    salt = uuid.uuid4().hex
    hashpswd = hashed_password(password, salt)

    #connect to database
    cnx = get_db()
    query = ''' INSERT INTO user (username,password,salt) VALUES (%s, %s, %s)'''
    cnx.cursor().execute(query,(username, hashpswd, salt))
    cnx.commit()

    #make a user dict
    ROOT_PATH = os.path.join(os.path.dirname(__file__),'static')
    PATH_USER = os.path.join(ROOT_PATH,username)
    os.mkdir(PATH_USER)

def check_name(username):
    cnx = get_db()
    cursor = cnx.cursor()
    query = '''SELECT * FROM user WHERE username = %s'''
    cursor.execute(query, (username,))
    row = cursor.fetchone()
    return row

def check_password(username, password):
    # Create variables for easy access
    # Check if account exists using MySQL
    cnx = get_db()
    cursor = cnx.cursor()
    query = 'SELECT salt FROM user WHERE (username) = %s'
    cursor.execute(query, (username,))
    salts = cursor.fetchone()
    true_password = hashed_password(password, salts[0])

    query = 'SELECT * FROM user WHERE username = %s AND password = %s'
    cursor.execute(query, (username, true_password))
    # Fetch one record and return result
    return cursor.fetchone()


# If account exists in accounts table in out database

def save_file(username, file, filename):
    #save original file
    app_path = os.path.dirname(__file__)
    stat_path = os.path.join(app_path, 'static')
    USER_PATH = os.path.join(stat_path, username)
    PATH = os.path.join(USER_PATH, filename)
    file.save(PATH)

    #save ocr file
    detection_img = text_detection.ap()
    detection_img.img = PATH
    ocr_PATH = detection_img.rectangle_image()

    #save thumbnail file
    thumbnails(PATH)
