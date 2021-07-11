import sqlite3
from typing import List, Any


class Staff:
    def __init__(self, staffID,
                 firstName, lastName,
                 email, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager):
        self.staffID = staffID
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.contactNumber = contactNumber
        self.address = address
        self.suburb = suburb
        self.postcode = postcode
        self.state = state
        self.dob = dob
        self.isManager = isManager


class StaffModel:
    _dbConn: sqlite3.Connection

    def __init__(self, dbConn):
        self._dbConn = dbConn

    def signIn(self, staffID, password):
        """Sets the session userid
        and returns True if the credentials are valid

        Returns False if the credentials are invalid"""
        cursor = self._dbConn.cursor()
        sql = """
            SELECT 1
            FROM Staff
            WHERE staffID = ? AND password = ?"""
        cursor.execute(sql, (staffID, password))
        row = cursor.fetchone()
        if row:
            return True
        else:
            return False

    def __convertStaffRow(self, row: List[Any]):
        return Staff(row[0], row[1], row[2],
                     row[3], row[5], row[6], row[7],
                     row[8], row[9], row[10], row[11])

    def createStaffMember(self,
                 firstName, lastName,
                 email, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager):
        password = "password"  # TODO: Randomly generate password

        cursor = self._dbConn.cursor()
        cursor.execute(
            """INSERT INTO Staff (
                 firstName, lastName,
                 email, password, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            , (firstName, lastName,
                 email, password, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager)
        )

        self._dbConn.commit()

        staffID = cursor.lastrowid
        return Staff(staffID, firstName, lastName,
                 email, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager)

    def getStaffMember(self, staffID):
        """Returns a Staff object based on the session user id

        Returns False if no staff infomation is found"""

        cursor = self._dbConn.cursor()
        cursor.execute(
            "SELECT * FROM staff WHERE staffID = ?", (staffID,)
        )

        row = cursor.fetchone()
        if row == None:
            raise Exception(f"ticket with staffID: {staffID} not found")

        return self.__convertStaffRow(row)

    def getStaffMembers(self):

        cursor = self._dbConn.cursor()
        cursor.execute(
            "SELECT * FROM staff"
        )

        rows = cursor.fetchall()
        if len(rows) == 0:
            raise Exception(f"no rows found")

        staffMembers = []
        for row in rows:
            staffMembers.append(self.__convertStaffRow(row))

        return staffMembers

    def updateStaffMember(self, staffID,
                 firstName, lastName,
                 email, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager):
        cursor = self._dbConn.cursor()
        # TODO: better way of doing this?
        cursor.execute(
            """UPDATE Staff
                SET firstName = ?,
                lastName = ?,
                email = ?,
                contactNumber = ?,
                address = ?,
                suburb = ?,
                postcode = ?,
                state = ?,
                dob = ?,
                isManager = ?
               WHERE staffID = ?
            """
            , (firstName, lastName,
                 email, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager,
                 staffID)
        )

        self._dbConn.commit()
