from datetime import datetime


class PayrollQuery:
    def __init__(self, payrollID, staffID, date, status, shifts):
        self.payrollID = payrollID
        self.staffID = staffID
        self.date = date
        self.status = status
        self.shifts = self.shifts


class PayrollQueryModel:
    def __init__(self, dbConn):
        self._dbConn = dbConn

    def createPayrollQuery(self, staffID, week, shifts):
        cursor = self._dbConn.cursor()
        cursor.execute("""INSERT INTO Payroll_Query (staffID, date, status) VALUES (?, 'now', 0)""", (staffID,))
        self._dbConn.commit()
        payrollID = cursor.lastrowid

        for shift in shifts:
            date = datetime.strptime(f"2021 {week} {shift['dayName']} {shift['startTime'] + 9}", "%Y %W %a %H")  # bajesus this hack
            cursor.execute("""INSERT INTO Payroll_Query_Details (payrollID, startTime, duration) VALUES (?, ?, ?)""", (payrollID, date, shift['duration']))
        self._dbConn.commit()
