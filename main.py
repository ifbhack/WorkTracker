# GLOBAL
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import configparser

# LOCAL
import functions

# INIT
app = Flask(__name__)
mysql = MySQL(app)
app.secret_key = 'admin'
SESSION_TYPE = 'redis'
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

# MANAGER/EMPLOYEE LOGIN
@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index-home.html')

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
  if request.method == 'POST':
    if functions.userSignIn(mysql):

      return redirect(url_for('homepage'))
    else:
      return 'Login Failed'
  
  return render_template('index-signIn.html')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
  if request.method == 'POST':
    session['userIDs'], session['name'], session['roleName'] = functions.userSignUp(mysql)
    return redirect(url_for('homepage'))

  cur = mysql.connection.cursor()
  cur.execute("""SELECT roleName FROM Payrate""")
  role_list = cur.fetchall()
  cur.connection.commit()
  cur.close()
  
  return render_template('index-signUp.html', role_list=role_list)

@app.route('/homepage')
def homepage():
  name, userID, roleName = session['name'], session['userIDs'], session['roleName']

  return f'employee by the name of {name} with the ID {userID} and role {roleName}' 

# MAIN
if __name__ == '__main__':
    app.run(host='0.0.0.0')
