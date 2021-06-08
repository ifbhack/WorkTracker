# GLOBAL IMPORTS
from flask import session


class Staff:
    def __init__(self, name, roleName):
        self.name = name
        self.roleName = roleName

    @staticmethod
    def __setUserId(userId):
        session['userId'] = userId

    @staticmethod
    def signIn(mysql, staffId, password):
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
        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO Staff (roleName, name, password)
                    VALUES (%s, %s, SHA2(%s, 256))""",
                    (roleName, name, password))
        mysql.connection.commit()
        staffId = cur.lastrowid
        cur.close()
        return staffId

    @staticmethod
    def get(mysql):
        userId = session.get('userId')
        if userId:
            cur = mysql.connection.cursor()
            cur.execute("""SELECT name, roleName FROM Staff
                            WHERE staffID = %s""", (userId))
            userDetails = cur.fetchone()
            cur.close()

            if userDetails:
                return Staff(*userDetails)
            else:
                return False
        else:
            return False
