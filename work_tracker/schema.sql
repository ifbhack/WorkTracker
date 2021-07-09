CREATE TABLE "Availability" (
    "staffID"    TEXT NOT NULL,
    "startTime"    TEXT NOT NULL,
    "duration"    TEXT NOT NULL,
    PRIMARY KEY("staffID","startTime"),
    FOREIGN KEY("staffID") REFERENCES "Staff"("staffID")
);

CREATE TABLE "Payroll_Query" (
    "payrollID"    INTEGER,
    "staffID"    INTEGER,
    "date"    TEXT,
    "status"    INTEGER,
    FOREIGN KEY("staffID") REFERENCES "Staff"("staffID"),
    PRIMARY KEY("payrollID" AUTOINCREMENT)
);

CREATE TABLE "Payroll_Query_Details" (
    "payrollID"    INTEGER,
    "startTime"    INTEGER,
    "duration"    INTEGER,
    FOREIGN KEY("payrollID") REFERENCES "Payroll_Query"("staffID")
);

CREATE TABLE "Roster" (
    "staffID"    INTEGER NOT NULL,
    "startTime"    TEXT NOT NULL,
    "duration"    INTEGER NOT NULL,
    FOREIGN KEY("staffID") REFERENCES "Staff"("staffID"),
    PRIMARY KEY("staffID")
);

CREATE TABLE "Staff" (
    "staffID"    INTEGER NOT NULL UNIQUE,
    "firstName"    TEXT NOT NULL,
    "lastName"    NUMERIC NOT NULL,
    "email"    TEXT NOT NULL UNIQUE,
    "contactNumber"    INTEGER NOT NULL,
    "address"    TEXT NOT NULL,
    "suburb"    TEXT NOT NULL,
    "postcode"    INTEGER NOT NULL,
    "state"    TEXT NOT NULL,
    "dob"    TEXT NOT NULL,
    "isManager"    INTEGER NOT NULL,
    PRIMARY KEY("staffID" AUTOINCREMENT)
);
