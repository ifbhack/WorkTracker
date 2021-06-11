from flask import session


class Staff:
    def __init__(self, userId, name, roleName, isManager):
        self.userId = userId
        self.name = name
        self.roleName = roleName
        self.isManager = isManager

    @staticmethod
    def __setUserId(userId):
        session['userId'] = userId

    @staticmethod
    def signIn(mysql, staffId, password):
        """Sets the session userid
        and returns True if the credentials are valid

        Returns False if the credentials are invalid"""
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
        """Inserts a new staff member into the database
        and sets the session userid to the created staff member"""
        cur = mysql.connection.cursor()
        cur.execute("""INSERT INTO Staff (roleName, name, password)
                    VALUES (%s, %s, SHA2(%s, 256))""",
                    (roleName, name, password))
        mysql.connection.commit()
        staffId = cur.lastrowid
        cur.close()
        Staff.__setUserId(staffId)

    @staticmethod
    def getObj(mysql):
        """Returns a Staff object based on the session user id

        Returns False if no staff infomation is found"""
        userId = session.get('userId')
        if userId:
            cur = mysql.connection.cursor()
            cur.execute("""SELECT name, roleName, isManager FROM Staff
                            WHERE staffID = %s""", (userId,))
            userDetails = cur.fetchone()
            cur.close()

            if userDetails:
                return Staff(userId, *userDetails)
            else:
                return False
        else:
            return False

    def getStaffPayInfo(self, mysql):
        cur = mysql.connection.cursor()
        DAYS_IN_MONTH = 30
        DAYS_IN_WEEK = 7
        hoursOfWorkPerDay = 8  # assume everyone work 8 hours a day for now
        sql = f"""SELECT payRate * {hoursOfWorkPerDay},
                         payRate * {hoursOfWorkPerDay} * {DAYS_IN_WEEK},
                         payRate * {hoursOfWorkPerDay} * {DAYS_IN_MONTH}
                  FROM Staff s
                  INNER JOIN Payrate p ON s.roleName=p.roleName
                  WHERE staffID = %s"""
        cur.execute(sql, (self.userId,))
        result = cur.fetchone()
        return {'daily': result[0], 'weekly': result[1], 'monthly': result[2]}

    def getRoster(self, mysql):
        """Returns the staff roster from the current week Monday to Sunday"""
        cur = mysql.connection.cursor()
        sql = """
            SELECT staffID, GROUP_CONCAT(DATE_FORMAT(date, '%a')) FROM Roster
            WHERE date BETWEEN SUBDATE(CURDATE(), WEEKDAY(CURDATE())) AND
                               ADDDATE(CURDATE(), 6 - WEEKDAY(CURDATE()))
            GROUP BY staffID"""
        cur.execute(sql)
        result = cur.fetchall()
        return result
