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
        self.suburb= suburb
        self.postcode = postcode
        self.state= state
        self.dob = dob
        self.isManager = isManager

class StaffModel:
    _db_conn: sqlite3.Connection


    def __init__(self, db_conn):
        self._db_conn = db_conn

    def signIn(self):
        """Sets the session userid
        and returns True if the credentials are valid

        Returns False if the credentials are invalid"""
        pass

    def signUp(self, name, password, roleName):
        """Inserts a new staff member into the database
        and sets the session userid to the created staff member"""
        pass

    def __convert_staff_row(self, row: List[Any]):
        return Staff(row[0], row[1], row[2], row[3],
                     row[4], row[5], row[6], row[7],
                     row[8], row[9], row[10])

    def createStaffMember(self, staffID,
                 firstName, lastName,
                 email, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager):

        cursor = self._db_conn.cursor()
        cursor.execute(
            """INSERT INTO Staff (staffID,
                 firstName, lastName,
                 email, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
            , (staffID, firstName, lastName,
                 email, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager)
        )

        self._db_conn.commit()

        return Staff(staffID, firstName, lastName,
                 email, contactNumber,
                 address, suburb,
                 postcode, state,
                 dob, isManager)

    def getStaffMember(self, staffID):
        """Returns a Staff object based on the session user id

        Returns False if no staff infomation is found"""

        cursor = self._db_conn.cursor()
        cursor.execute(
            "SELECT * FROM staff WHERE staffID = ?", (staffID,)
        )

        row = cursor.fetchone()
        if row == None:
            raise Exception(f"ticket with staffID: {staffID} not found")

        return self.__convert_staff_row(row)

    def getStaffMembers(self):

        cursor = self._db_conn.cursor()
        cursor.execute(
            "SELECT * FROM staff"
        )

        rows = cursor.fetchall()
        if len(rows) == 0:
            raise Exception(f"no rows found")

        staffMembers = []
        for row in rows:
            staffMembers.append(self.__convert_staff_row(row))

        return staffMembers

    def updateStaffMember(self, staffMember: Staff):
        cursor = self._db_conn.cursor()
        # TODO: better way of doing this?
        cursor.execute(
            """UPDATE Staff
                SET firstName = ?
                SET lastName = ?
                SET email = ?
                SET contactNumber = ?
                SET address = ?
                SET suburb = ?
                SET postcode = ?
                SET state = ?
                SET dob = ?
                SET isManager = ?
               WHERE staffID = ?
            """
            , (staffMember.firstName, staffMember.lastName,
                 staffMember.email, staffMember.contactNumber,
                 staffMember.address, staffMember.suburb,
                 staffMember.postcode, staffMember.state,
                 staffMember.dob, staffMember.isManager,
                 staffMember.staffID)
        )

        self._db_conn.commit()
