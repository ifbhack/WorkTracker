# LOCAL
from flask import Flask, render_template, request, redirect, url_for, g
from flask_mysqldb import MySQL
import MySQLdb
import configparser

from functions import Staff


# FLASK INIT
app = Flask(__name__)
app.secret_key = 'admin'
SESSION_TYPE = 'redis'

# SQL INIT
mysql = MySQL(app)
app.config.from_object(__name__)

config = configparser.ConfigParser()
if config.read('config.ini') == []:
    # create new config file
    config['mysql'] = {}
    mysql_config = config['mysql']
    mysql_config['username'] = 'root'
    mysql_config['password'] = 'secret'
    mysql_config['database'] = 'work_tracker'
    with open('config.ini', 'w') as f:
        config.write(f)
else:
    mysql_config = config['mysql']
    app.config['MYSQL_USER'] = mysql_config['username']
    app.config['MYSQL_PASSWORD'] = mysql_config['password']
    app.config['MYSQL_DB'] = mysql_config['database']


# Landing/Sign In Page
@app.route('/', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        try:
            success = Staff.signIn(mysql,
                                   staffId=request.form['staffid'],
                                   password=request.form['password'])
        except MySQLdb.Error:
            return 'Database Error'

        if success:
            return redirect(url_for('homepage'))
        else:
            return 'Login Failed'
    else:
        return render_template('index-signIn.html')


# LANDING PAGE FOR LOGGED IN USERS
@app.route('/homepage')
def homepage():
    if g.user:
        payInfo = g.user.getStaffPayInfo(mysql)
        roster = g.user.getRoster(mysql)
        return render_template('index-home.html', name=g.user.name, isManager=g.user.isManager)
    else:
        return "Not logged in"


@app.before_request
def getUserInfo():
    """Sets g.user to a Staff object before every page request

    Sets g.user to None if the user is not signed in"""
    try:
        user = Staff.getObj(mysql)
    except MySQLdb.Error:
        return 'Database Error'

    if user:
        g.user = user
    else:
        g.user = None


# MAIN
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
