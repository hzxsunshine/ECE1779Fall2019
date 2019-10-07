from flask import Flask, render_template, request, redirect, url_for, session
import re
from .database import connect_to_database,  get_db, teardown_db
from app import webapp
from .utils import check_name, save_reg

@webapp.route('/login', methods=['GET', 'POST'])
def login():
    if 'Authenticated' in session:
        return redirect(url_for('upload'))
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cnx = get_db()
        cursor = cnx.cursor()
        query = 'SELECT * FROM user WHERE username = %s AND password = %s'
        cursor.execute(query, (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['Authenticated'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('main'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@webapp.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('Authenticated', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

    

@webapp.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'repassword' in request.form:
        if request.form['password'] != request.form['repassword']:
            msg = 'Password and Repeated Password Should Be the Same!'
        # check the availability of username
        elif check_name(request.form['username']) is not None:
            msg = 'Choose Another Cool Username Please!'
        else:
            # Create variables for easy access
            username = request.form['username']
            password = request.form['password']
            save_reg(username,password)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# @webapp.route('/')
# @webapp.route('/index')
# def index():
#     if 'Authenticated' not in session:
#         return redirect(url_for('login'))
#     
#     posts = [
#         {
#             'author': {'username': 'SunShine'},
#             'body': 'She will be back, I thought.'
#         }
#     ]
#     return render_template('index.html', title='Home', posts=posts)

