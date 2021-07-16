from datetime import datetime

# !! All this code is very similar to the timesheet model
# I'm too lazy to figure out how to share code properly rn


class Shift:
    def __init__(self, startTime, duration):
        self.startTime = startTime
        self.duration = duration


class RosterModel:
    timeOffset = 9

    def __init__(self, dbConn):
        self._dbConn = dbConn

    def __convertStaffRow(self, row):
        startTime = datetime.strptime(row[0], "%Y-%m-%d %H:%M")
        return Shift(startTime, row[1])

    def getRoster(self, staffID, startTime, endTime):
        cursor = self._dbConn.cursor()
        cursor.execute("""
            SELECT startTime, duration
            FROM Roster
            WHERE 
                staffID = ? AND
                startTime BETWEEN ? AND ?""", (staffID, startTime, endTime))
        rows = cursor.fetchall()
        shifts = []
        for row in rows:
            shifts.append(self.__convertStaffRow(row))
        return shifts

    def shiftsToJson(self, shifts):
        jsonShifts = []
        for shift in shifts:
            jsonShift = {}
            jsonShift['dayName'] = shift.startTime.strftime("%a")
            jsonShift['startTime'] = int(shift.startTime.strftime("%H")) - self.timeOffset
            jsonShift['duration'] = shift.duration
            jsonShifts.append(jsonShift)
        return jsonShifts
