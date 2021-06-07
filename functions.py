from flask import Flask, render_template, request
import random

userIDs = []

def userSignIn():
    name, password = request.form['name'], request.form['password']
    
    if checkUser(name, password):
        return 'Login successful'
    else:
        return 'Login failed due to incorrect login details'

def userSignUp():
    name, password = request.form['name'], request.form['password']
    
    if name[0].upper() == 'E':
        password = hashPassword(password)
        userID = generateUserID()
        storeUserData(name, password, userID)
        return name, userID
    elif name[0].upper() == 'M':
        password = hashPassword(password)
        userID = generateUserID()
        storeUserData(name, password, userID)
        return name, userID
    else:
        return 'Login failed due to the username not prefixed with either "e:" or "m:"'

def checkUser(name, password):
    # Check details in database | will return True or False
    pass

def hashPassword(password):
    # Hash password
    pass

def generateUserID():
    global userIDs

    if len(userIDs) == 0:
        userIDs.append('000001')
    else:
        userIDs.append(str(int(userIDs[len(userIDs) - 1]) + 1).zfill(6))

    return userIDs[len(userIDs)-1]

def storeUserData(name, password, userID):
    # Insert data into the database
    pass

def generateWorkplaceID():
    pass
