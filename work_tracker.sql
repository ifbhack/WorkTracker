DROP DATABASE IF EXISTS Work_Tracker;
CREATE DATABASE IF NOT EXISTS Work_Tracker;

USE Work_Tracker;

CREATE TABLE IF NOT EXISTS Employee (
	employeeID INT(10) ZEROFILL AUTO_INCREMENT,
    Name VARCHAR(30) NOT NULL,
    Password VARCHAR(30) NOT NULL, 
    PRIMARY KEY (employeeID)
);

CREATE TABLE IF NOT EXISTS Manager (
	managerID INT(10) ZEROFILL AUTO_INCREMENT,
    NAME VARCHAR(30) NOT NULL,
    Password VARCHAR(30) NOT NULL,
    PRIMARY KEY (employeeID)
); 

INSERT INTO Employee (Name) VALUES ('Toni');


#SELECT * FROM Employee;
#CREATE TABLE IF NOT EXISTS Manager (
#	managerID 
#);

