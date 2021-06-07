from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index-login.html')

@app.route('/', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    name, password = request.form['name'], request.form['password']
    
    if name[0].upper() == 'E':
      return f'Employee with the name: {name[2:]}'
    elif name[0].upper() == 'M':
      return f'Manager with the name: {name[2:]}'
    else:
      return 'Login failed due to incorrect login details or due to the username not prefixed with either "e:" or "m:"'

  return render_template('index-login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
