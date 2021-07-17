INSERT INTO Staff VALUES (1, 'Joe', 'Hilbert', 'joe.hilbert@email.com', 'password', 0429392183, '7 Tiger St', 'Kooringal', 4025, 'QLD', '2016-08-30', False);
INSERT INTO Staff VALUES (2, 'Bob', 'Row', 'bob.row@email.com', 'password', 0424592183, '45 YouWho Lane', 'Somewhat', 4157, 'QLD', '1910-08-30', True);
INSERT INTO Staff VALUES (3, 'Rob', 'Jones', 'rob.jones@email.com', 'password', 04223245654, '34 What Street', 'Vandan', 4564, 'QLD', '1782-08-30', False);

INSERT INTO Timesheet VALUES (1, '2021-07-08 09:00', 5);

INSERT INTO Roster VALUES (1, '2021-07-08 09:00', 7);

INSERT INTO Payroll_Query VALUES (1, 1, date('now'), 0);
INSERT INTO Payroll_Query_Details VALUES (1, '2021-07-08 09:00', 4);
