DROP TABLE IF EXISTS "Roster";
DROP TABLE IF EXISTS "Availability";
DROP TABLE IF EXISTS "Staff";
DROP TABLE IF EXISTS "Payroll_Query";
DROP TABLE IF EXISTS "Payroll_Query_Details";
DROP TABLE IF EXISTS "Timesheet";

CREATE TABLE IF NOT EXISTS "Roster" (
	"staffID"	INTEGER NOT NULL,
	"startTime"	TEXT NOT NULL,
	"duration"	INTEGER NOT NULL,
	FOREIGN KEY("staffID") REFERENCES "Staff"("staffID"),
	PRIMARY KEY("staffID")
);

CREATE TABLE IF NOT EXISTS "Availability" (
	"staffID"	TEXT NOT NULL,
	"startTime"	TEXT NOT NULL,
	"duration"	TEXT NOT NULL,
	FOREIGN KEY("staffID") REFERENCES "Staff"("staffID"),
	PRIMARY KEY("staffID","startTime")
);

CREATE TABLE IF NOT EXISTS "Staff" (
	"staffID"	INTEGER NOT NULL UNIQUE,
	"firstName"	TEXT NOT NULL,
	"lastName"	NUMERIC NOT NULL,
	"email"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	"contactNumber"	INTEGER NOT NULL,
	"address"	TEXT NOT NULL,
	"suburb"	TEXT NOT NULL,
	"postcode"	INTEGER NOT NULL,
	"state"	TEXT NOT NULL,
	"dob"	TEXT NOT NULL,
	"isManager"	INTEGER NOT NULL,
	PRIMARY KEY("staffID" AUTOINCREMENT)
);

CREATE TABLE IF NOT EXISTS "Payroll_Query" (
	"payrollID"	INTEGER NOT NULL,
	"staffID"	INTEGER NOT NULL,
	"date"	TEXT NOT NULL,
	"status"	INTEGER NOT NULL,
	PRIMARY KEY("payrollID" AUTOINCREMENT),
	FOREIGN KEY("staffID") REFERENCES "Staff"("staffID")
);

CREATE TABLE IF NOT EXISTS "Payroll_Query_Details" (
	"payrollID"	INTEGER NOT NULL,
	"startTime"	INTEGER NOT NULL,
	"duration"	INTEGER NOT NULL,
	FOREIGN KEY("payrollID") REFERENCES "Payroll_Query"("staffID")
);

CREATE TABLE IF NOT EXISTS "Timesheet" (
	"staffID"	INTEGER NOT NULL,
	"startTime"	TEXT NOT NULL,
	"duration"	INTEGER NOT NULL,
	PRIMARY KEY("staffID","startTime"),
	FOREIGN KEY("staffID") REFERENCES "Staff"("staffID")
);
