
# GLOBAL IMPORTS
from flask import Flask, render_template, request, session
from passlib.context import CryptContext # pip install passlib
import random


# INIT FOR PASSWORD HASHING
pwd_context = CryptContext(
    schemes = ['pbkdf2_sha256'],
    default = 'pbkdf2_sha256',
    pbkdf2_sha256__default_rounds=30000
)


# FUNCTION TO SIGN THE USER IN
def userSignIn(mysql):
    userID, password = request.form['name'], request.form['password']

    if checkUser(userID, password, mysql):
        return True
    else:
        return False


# FUNCTION TO CREATE A USER ACCOUNT
def userSignUp(mysql):
    name, password, roleName = request.form['name'] , request.form['password'], request.form.get('roleName')

    password = hashPassword(password)
    userID = storeUserData(name, password, roleName, mysql)
    return userID, name, roleName


# FUNCTION TO CHECK IF USER HAS ALREADY BEEN CREATED 
def checkUser(userID, password, mysql):
    try:

        cur = mysql.connection.cursor()
        # cur.execute(f"""SELECT staffID, name, password, roleName FROM Staff WHERE staffID = '{userID}' AND password = '{password}'""")
        cur.execute(f'SELECT password FROM Staff WHERE staffID = "{userID}"')
        
        if pwd_context.verify(password, cur.fetchone()[0]):
            cur.execute(f'SELECT staffID, name, roleName FROM Staff WHERE staffID = "{userID}"')
            userData = cur.fetchone()
            session['userIDs'], session['name'], session['roleName'] = userData
            cur.close()
            return True
        else:
            return False
    except:
        return False


# FUNCTION TO HASH THE USERS PASSWORD
def hashPassword(password):
    password = pwd_context.hash(password)
    return password


# FUNCTION TO STORE ALL USER DATA INTO THE DATABASE
def storeUserData(name, password, roleName, mysql):
    cur = mysql.connection.cursor()

    cur.execute(f'INSERT INTO Staff (roleName, name, password) VALUES ("{roleName}", "{name}", "{password}")')
    cur.connection.commit()

    cur.close()

    return cur.lastrowid # This is the user ID
        