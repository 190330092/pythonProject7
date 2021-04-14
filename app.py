from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector as b
import mysql.connector
import re
app = Flask(__name__)
app.secret_key = '@#hyd*'
mydb = b.connect(host="localhost",user="root",password="190330092",database="ugrocer")
mycursor = mydb.cursor(app)
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'Email id ' in request.form and 'password' in request.form:
        Email_id = request.form['Email id']
        password = request.form['password']
        mycursor = mydb.cursor(dictionary=True)
        #mycursor =mydb.cursor(mydb.DictCursor)_
        mycursor.execute('SELECT * FROM accounts WHERE Email_id = %s AND password = %s', (Email_id, password,))
        account = mycursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            msg = 'Logged in successfully !'
            return render_template('home.html', msg=msg)
        else:
            msg = 'Incorrect username / password !'
    return render_template("login.html", msg=msg)
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('Email_id', None)
    return redirect(url_for('login'))
@app.route("/register", methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'First_Name' in request.form and 'Last_Name' in request.form and 'Email_id' in request.form and 'password' in request.form:
        First_Name = request.form["First Name"]
        Last_Name = request.form["Last Name"]
        Email_id = request.form["Email id"]
        password = request.form["password"]
        #mycursor = mydb.cursor(mydb.DictCursor)
        mycursor = mydb.cursor(dictionary=True)
        mycursor.execute("SELECT * FROM accounts WHERE  = %s", (username,))
        account = mycursor.fetchone()
        if account:
            msg = 'account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            mycursor.execute("INSERT INTO accounts VALUES (NULL, %s, %s, %s)", (username, password, email,))
            mydb.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template("register.html", msg=msg)
if __name__=='__main__':
    app.run(debug=True)