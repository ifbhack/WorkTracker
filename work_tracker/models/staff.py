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
                         row[3], row[5], row[6],
                         row[7], row[8], row[9],
                         row[10], row[11])

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

    def __getStaffMembers(self, sqlCondition, params):

        if sqlCondition == "":
            query = "SELECT * FROM staff"
        else:
            query = f"SELECT * FROM staff WHERE {sqlCondition}"

        cursor = self._dbConn.cursor()
        cursor.execute(query, params)

        rows = cursor.fetchall()
        if len(rows) == 0:
            raise Exception(f"no rows found")

        staffMembers = []
        for row in rows:
            staffMembers.append(self.__convertStaffRow(row))

        return staffMembers


    def getStaffMembers(self):
        return self.__getStaffMembers("", ())

    def getStaffMembersByName(self, name):
        # NOTE: sqlite doesn't like "%?%" so we do the madness below.

        return self.__getStaffMembers("firstName LIKE ? OR lastName LIKE ?",
                                      ('%'+name+'%', '%'+name+'%'))

    # NOTE: below looks a bit ugly, might want to refactor later

    def getStaffMembersByEmail(self, email):
        return self.__getStaffMembers("email LIKE ?", ('%'+email+'%',))

    def getStaffMembersByContactNumber(self, contactNumber):
        return self.__getStaffMembers("contactNumber LIKE ?", ('%'+contactNumber+'%',))

    def getStaffMembersByAddress(self, address):
        return self.__getStaffMembers("address LIKE ?", ('%'+address+'%',))

    def getStaffMembersBySuburb(self, suburb):
        return self.__getStaffMembers("suburb LIKE ?", ('%'+suburb+'%',))

    def getStaffMembersByPostcode(self, postcode):
        return self.__getStaffMembers("postcode LIKE ?", ('%'+postcode+'%',))

    def getStaffMembersByState(self, state):
        return self.__getStaffMembers("state LIKE ?", ('%'+state+'%',))

    def getStaffMembersByDOB(self, dob):
        return self.__getStaffMembers("dob LIKE ?", ('%'+dob+'%',))

    def getStaffMembersByLevel(self, level):
        return self.__getStaffMembers("isManager = ?", (level,))

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
