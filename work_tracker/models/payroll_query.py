from datetime import datetime


class Shift:
    def __init__(self, startTime, duration):
        self.startTime = startTime
        self.duration = duration


class PayrollQuery:
    def __init__(self, payrollID, staffID, date, status, shifts):
        self.payrollID = payrollID
        self.staffID = staffID
        self.date = date
        self.status = status
        self.shifts = self.shifts


class PayrollQueryModel:
    timeOffset = 9

    def __init__(self, dbConn):
        self._dbConn = dbConn

    def __convertStaffRow(self, row):
        startTime = datetime.strptime(row[0], "%Y-%m-%d %H:%M")
        return Shift(startTime, row[1])

    def createPayrollQuery(self, staffID, week, shifts):
        cursor = self._dbConn.cursor()
        cursor.execute("""INSERT INTO Payroll_Query (staffID, date, status) VALUES (?, date('now'), 0)""", (staffID,))
        self._dbConn.commit()
        payrollID = cursor.lastrowid

        for shift in shifts:
            date = datetime.strptime(f"2021 {week} {shift['dayName']} {shift['startTime'] + self.timeOffset}", "%Y %W %a %H")  # bajesus this hack
            cursor.execute("""INSERT INTO Payroll_Query_Details (payrollID, startTime, duration) VALUES (?, ?, ?)""", (payrollID, date, shift['duration']))
        self._dbConn.commit()

    def getPayrollQueryDetails(self, payrollID):
        cursor = self._dbConn.cursor()
        cursor.execute("""
            SELECT startTime, duration FROM Payroll_Query_Details
            WHERE payrollID = ?""", (payrollID,))
        rows = cursor.fetchall()
        shifts = []
        for row in rows:
            shifts.append(self.__convertStaffRow(row))
        return shifts

    def approvePayrollQuery(self, payrollID):
        cursor = self._dbConn.cursor()
        cursor.execute("""
            UPDATE Payroll_Query SET status = 1
            WHERE payrollID = ?""", (payrollID,))
        self._dbConn.commit()

    def shiftsToJson(self, shifts):
        jsonShifts = []
        for shift in shifts:
            jsonShift = {}
            jsonShift['dayName'] = shift.startTime.strftime("%a")
            jsonShift['startTime'] = int(shift.startTime.strftime("%H")) - self.timeOffset
            jsonShift['duration'] = shift.duration
            jsonShifts.append(jsonShift)
        return jsonShifts
