
# GLOBAL
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import configparser


# LOCAL
import functions


# INIT

# FLASK INIT
app = Flask(__name__)
app.secret_key = 'admin'
SESSION_TYPE = 'redis'


#SQL INIT
mysql = MySQL(app)
app.config.from_object(__name__)
config = configparser.ConfigParser()
config.read('config.ini')

if 'mysql' in config:
  mysql_config = config['mysql']
  app.config['MYSQL_USER'] = mysql_config['username']
  app.config['MYSQL_PASSWORD'] = mysql_config['password']
  app.config['MYSQL_DB'] = mysql_config['database']
else:
  raise Exception('No mysql section in the config provided')


# FLASK FUNCTIONS

# MAIN LANDING PAGE
@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index-home.html')


# USER SIGN IN PAGE
@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
  if request.method == 'POST':
    # IF THE USER DETAILS ARE CORRECT
    if functions.userSignIn(mysql):
      return redirect(url_for('homepage'))
    else:
      return 'Login Failed'
  
  return render_template('index-signIn.html')


# USER SIGN UP PAGE
@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
  if request.method == 'POST':
    # CREATE SESSION VARIABLES FOR USER
    session['userIDs'], session['name'], session['roleName'] = functions.userSignUp(mysql)
    return redirect(url_for('homepage'))

  # DISPLAY DATA FOR USER SELECTABLE ROLES BASED OFF DATABASE INFORMATION
  cur = mysql.connection.cursor()
  cur.execute("""SELECT roleName FROM Payrate""")
  role_list = cur.fetchall()
  cur.connection.commit()
  cur.close()
  
  return render_template('index-signUp.html', role_list=role_list)


# LANDING PAGE FOR LOGGED IN USERS
@app.route('/homepage')
def homepage():
  name, userID, roleName = session['name'], session['userIDs'], session['roleName']
  user_details = [name, userID, roleName]
  return render_template('homepage.html', user_details = user_details)
  

# MAIN
if __name__ == '__main__':
    app.run(host='0.0.0.0')
