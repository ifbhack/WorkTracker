# GLOBAL
from flask import Flask, render_template, request, redirect, url_for, session

# LOCAL
import functions

# INIT
app = Flask(__name__)
app.secret_key = 'admin'
SESSION_TYPE = 'redis'
app.config.from_object(__name__)

# FLASK FUNCTIONS

# MANAGER/EMPLOYEE LOGIN
@app.route('/', methods=['GET', 'POST'])
def signIn():
  if request.method == 'POST':
    return functions.userSignIn()
  
  return render_template('index-signIn.html')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
  if request.method == 'POST':
    session['name'], session['userIDs'] = functions.userSignUp()
    return redirect(url_for('homepage'))
  
  return render_template('index-signUp.html')

@app.route('/homepage')
def homepage():
  name, userID= session['name'], session['userIDs']

  if 'e:' in session['name']:
    return f'employee by the name of {name[2:]} with the ID {userID}'
  elif 'm:' in session['name']:
    return f'manager by the name of {name[2:]} with the ID {userID}' 
  else:
    return 'error'
  

# MAIN
if __name__ == '__main__':
    app.run(host='0.0.0.0')
