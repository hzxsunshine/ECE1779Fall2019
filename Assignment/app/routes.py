from flask import Flask, render_template, request, redirect, url_for, session
import re
from .database import connect_to_database,  get_db, teardown_db
from app import webapp
from .utils import check_name, save_reg, check_password

@webapp.route('/login', methods=['GET', 'POST'])
def login():
    if 'Authenticated' in session:
        return redirect(url_for('upload'))
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        account = check_password(request.form['username'],request.form['password'])
        
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
            msg = 'Successful Registered'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)
