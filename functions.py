# GLOBAL IMPORTS
from flask import session


class Staff:
    def __init__(self, name, roleName, isManager):
        self.name = name
        self.roleName = roleName
        self.isManager = isManager

    @staticmethod
    def __setUserId(userId):
        session['userId'] = userId

    @staticmethod
    def signIn(mysql, staffId, password):
        # Sets the session userid
        # and returns True if the credentials are valid
        # Returns False if the credentials are invalid
        
        cur = mysql.connection.cursor()
        cur.execute("""SELECT 1 FROM Staff
                    WHERE staffID = %s AND password = SHA2(%s, 256)""",
                    (staffId, password))
        validCredentials = cur.fetchone()
        cur.close()

        if validCredentials:
            Staff.__setUserId(staffId)
            return True
        else:
            return False

    @staticmethod
    def signUp(mysql, name, password, roleName):
        # Inserts a new staff member into the database
        # and sets the session userid to the created staff member

        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO Staff (roleName, name, password)
                    VALUES (%s, %s, SHA2(%s, 256))""",
                    (roleName, name, password))
        mysql.connection.commit()
        staffId = cur.lastrowid
        cur.close()
        Staff.__setUserId(staffId)

    @staticmethod
    def get(mysql):
        # Returns a Staff object based on the session user id
        # Returns False if no staff infomation is found

        userId = session.get('userId')
        if userId:
            cur = mysql.connection.cursor()
            cur.execute("""SELECT name, roleName, isManager FROM Staff
                            WHERE staffID = %s""", (userId,))
            userDetails = cur.fetchone()
            cur.close()

            if userDetails:
                return Staff(*userDetails)
            else:
                return False
        else:
            return False
