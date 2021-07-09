USE Work_Tracker;

# Finding a calculated amount of pay for one day
SELECT staffID, SUM(payRate * duration) 'Daily_Earnings'
FROM Roster 
NATURAL JOIN Staff 
NATURAL JOIN Payrate
GROUP BY StaffID;

# Finding gross pay for all-time
SELECT staffID, DAY(date), SUM(payRate * duration) 'Weekly_Earnings'
FROM Roster 
NATURAL JOIN Staff 
NATURAL JOIN Payrate
GROUP BY staffID;

# Finding gross pay per store
SELECT staffID, DAY(date), SUM(payRate * duration) 'Weekly_Earnings'
FROM Roster 
NATURAL JOIN Staff 
NATURAL JOIN Payrate
WHERE roster.workplaceID LIKE 1 # In store number 1
GROUP BY staffID;

# Number of shifts worked so far, with total number of hours worked
SELECT COUNT(staffID), SUM(duration)
FROM Roster 
NATURAL JOIN Staff 
GROUP BY staffID;


# Finding a calculated amount of pay for one week (Putting this on hold as I need a base date to compare with)
-- SELECT staffID, DAY(date), SUM(payRate * duration) 'Weekly_Earnings'
-- FROM Roster 
-- NATURAL JOIN Staff 
-- NATURAL JOIN Payrate
-- WHERE DAY(date) BETWEEN DAY(date) AND (DAY(date) + 6)
-- GROUP BY staffID, date;

#WHERE day(date) BETWEEN DAY(date) AND DAY(date + 7)
# Roster -> Staff -> Payrate
