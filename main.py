from flask import Flask, render_template, request, redirect, url_for, g
from flask_mysqldb import MySQL
import MySQLdb
import configparser

# LOCAL
from functions import Staff


# INIT

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


# MAIN LANDING PAGE
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index-home.html')


# USER SIGN IN PAGE
@app.route('/signIn', methods=['GET', 'POST'])
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


# USER SIGN UP PAGE
@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        try:
            Staff.signUp(mysql,
                         name=request.form['name'],
                         password=request.form['password'],
                         roleName=request.form['roleName'])
        except MySQLdb.Error:
            return 'Database Error'

        return redirect(url_for('homepage'))
    else:
        # DISPLAY DATA FOR USER SELECTABLE ROLES BASED OFF DATABASE INFORMATION
        try:
            cur = mysql.connection.cursor()
            cur.execute('SELECT roleName FROM Payrate')
            role_list = cur.fetchall()
            cur.close()
        except MySQLdb.Error:
            return 'Database Error'

        return render_template('index-signUp.html', role_list=role_list)


# LANDING PAGE FOR LOGGED IN USERS
@app.route('/homepage')
def homepage():
    if g.user:
        if g.user.isManager:
            return "Manager page"  # todo
        else:
            payInfo = g.user.getStaffPayInfo(mysql)
            roster = g.user.getRoster(mysql)
            return render_template('homepage-employee.html',
                                   payInfo=payInfo,
                                   roster=roster)
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
