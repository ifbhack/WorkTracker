DROP DATABASE IF EXISTS Work_Tracker;
CREATE DATABASE IF NOT EXISTS Work_Tracker;

USE Work_Tracker;

CREATE TABLE IF NOT EXISTS Payrate (
	roleName VARCHAR(15) NOT NULL,
    payRate DECIMAL(5, 2) NOT NULL,
	PRIMARY KEY (roleName)
);

CREATE TABLE IF NOT EXISTS Staff (
	staffID INT(4) AUTO_INCREMENT,
    roleName VARCHAR(15) DEFAULT 'Floor Worker',
    name VARCHAR(20) NOT NULL,
    password VARCHAR(30) NOT NULL,
    isManager BOOL DEFAULT 0,
    PRIMARY KEY (staffID),
    FOREIGN KEY (roleName) REFERENCES Payrate (roleName)
);

CREATE TABLE IF NOT EXISTS Workplace (
	workplaceID INT NOT NULL AUTO_INCREMENT,
    managerID INT NOT NULL,
    PRIMARY KEY (workplaceID),
    FOREIGN KEY (managerID) REFERENCES Staff (staffID)
);

CREATE TABLE IF NOT EXISTS Roster (
	staffID INT NOT NULL,
    date DATE NOT NULL,
    workplaceID INT NOT NULL,
    duration INT NOT NULL,
    PRIMARY KEY (staffID, date),
    FOREIGN KEY (staffID) REFERENCES Staff (staffID),
    FOREIGN KEY (workplaceID) REFERENCES Workplace (workplaceID)
); 

INSERT INTO Payrate VALUES ('Floor Worker', 10.12)

