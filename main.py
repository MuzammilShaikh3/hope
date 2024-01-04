from flask import Flask, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib



app = Flask(__name__, template_folder='template')
app.secret_key = 'fdafadfqaerhgu'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Mroot@396'
# app.config['MYSQL_DB'] = 'co'

app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12674420'
app.config['MYSQL_PASSWORD'] = 'fyVaeJ2Xug'
app.config['MYSQL_DB'] = 'sql12674420'

mysql = MySQL(app)
 

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login2 WHERE username = % s AND pass = % s', (username, password ))
        loginstd = cursor.fetchone()
        if loginstd:
            session['loggedin'] = True
            session['id'] = loginstd['id']
            session['username'] = loginstd['username']
            # sendemail ="hopehelps36@gmail.com"
            
            print(email)
            password= "Zuber123"
            message ="You just Logged Into HOPE"

            # server =smtplib.SMTP('smtp.gmail.com', 587)
            # server.starttls ()
            # server.login (sendemail, password)
            print ("Login success")
            # server.sendmail (sendemail, email, message)
            # print ("Email has been sent to ", email)
            return render_template('index.html', username= username)
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)

 
@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/')
def parallax():
    return render_template('parallax.html')

@app.route('/pop')
def pop():
    return render_template('pop.html')


@app.route('/stress')
def stress():
    return render_template('stress.html')

@app.route('/Depression')
def Depression():
    return render_template('Depression.html')

@app.route('/Anxiety')
def Anxiety():
    return render_template('Anxiety.html')


@app.route('/story')
def story():
    return render_template('story.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login2 WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
             cursor.execute('INSERT INTO login2 VALUES (NULL, % s, % s, % s)', (username, password, email, ))
             mysql.connection.commit()
             sendemail ="hopehelps36@gmail.com"
            
             print(email)
             password= "Zuber123"
             message ="You have successfully registered to HOPE!"

             server =smtplib.SMTP('smtp.gmail.com', 587)
             server.starttls ()
             server.login (sendemail, password)
             print ("Login success")
             server.sendmail (sendemail, email, message)
             print ("Email has been sent to ", email)
             msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)


if __name__ == "__main__":
    app.run()