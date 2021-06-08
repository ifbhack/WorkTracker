from flask import Flask, render_template, request
import random

userIDs = []
userData = [] # 0 = id; 1 = name; 2 = password;

def userSignIn():
    global userID

    userID, password = request.form['name'], request.form['password']
    
    if checkUser(userID, password):
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

def checkUser(userID, password):
    global userData

    for i in userData:
        if userID == i[0] and password == i[2]:
            x = True
        else:
            x = False
        
    if x == False:
        return False
    else:
        return True
            

def hashPassword(password):
    # Hash password
    return password

def generateUserID():
    global userIDs

    if len(userIDs) == 0:
        userIDs.append('000001')
    else:
        userIDs.append(str(int(userIDs[len(userIDs) - 1]) + 1).zfill(6))

    return userIDs[len(userIDs)-1]

def storeUserData(name, password, userID):
    global userData

    if [name, password, userID] in userData:
        pass
    else:
        userData.append([userID, name, password])
        print(userData)
        

def generateWorkplaceID():
    pass
