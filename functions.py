from flask import Flask, render_template, request, session
import random


def userSignIn(mysql):
    userID, password = request.form['name'], request.form['password']

    if checkUser(userID, password, mysql):
        return True
    else:
        return False

def userSignUp(mysql):
    name, password, roleName = request.form['name'] , request.form['password'], request.form.get('roleName')

    password = hashPassword(password)
    userID = storeUserData(name, password, roleName, mysql)
    return userID, name, roleName

def checkUser(userID, password, mysql):
    try:
        cur = mysql.connection.cursor()
        cur.execute(f"""SELECT staffID, name, password, roleName FROM Staff WHERE staffID = '{userID}' AND password = '{password}'""")
        userData = cur.fetchone()

        session['userIDs'], session['name'], session['roleName'] = userData[0], userData[1], userData[3]
        cur.close()
        return True
    except:
        return False

def hashPassword(password):
    # Hash password
    return password

def storeUserData(name, password, roleName, mysql):
    cur = mysql.connection.cursor()

    cur.execute("""INSERT INTO Staff (roleName, name, password) VALUES (%s, %s, %s)""", (roleName, name, password))
    cur.connection.commit()

    cur.close()

    return cur.lastrowid # This is the user ID
        