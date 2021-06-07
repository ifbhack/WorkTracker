# GLOBAL
from flask import Flask, render_template, request, redirect, url_for

# LOCAL
import functions

# INIT
app = Flask(__name__)

# FLASK FUNCTIONS

# MANAGER/EMPLOYEE LOGIN
@app.route('/', methods=['GET', 'POST'])
def signIn():
  if request.method == 'POST':
    return functions.userSignIn()
  
  return render_template('index-signIn.html')

@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
  global name

  if request.method == 'POST':
    name = functions.userSignUp()
    return redirect(url_for('homepage'))
  
  return render_template('index-signUp.html')

@app.route('/homepage')
def homepage():
  if 'e:' in name:
    return f'employee by the name of {name[2:]}'
  elif 'm:' in name:
    return f'manager by the name of {name[2:]}' 
  else:
    return 'error'
  

# MAIN
if __name__ == '__main__':
    app.run(host='0.0.0.0')
