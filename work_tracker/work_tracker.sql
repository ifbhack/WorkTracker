DROP DATABASE IF EXISTS Work_Tracker;
CREATE DATABASE IF NOT EXISTS Work_Tracker;

USE Work_Tracker;

# Create tables
CREATE TABLE IF NOT EXISTS Payrate (
	roleName VARCHAR(15) NOT NULL,
    payRate DECIMAL(5, 2) NOT NULL,
	PRIMARY KEY (roleName)
);

CREATE TABLE IF NOT EXISTS Staff (
	staffID INT(4) AUTO_INCREMENT,
    roleName VARCHAR(15),
    name VARCHAR(20) NOT NULL,
    password CHAR(64) NOT NULL, -- hash length is 64
    isManager BOOL DEFAULT 0,
    PRIMARY KEY (staffID),
    FOREIGN KEY (roleName) REFERENCES Payrate (roleName)
);

CREATE TABLE IF NOT EXISTS Workplace (
	workplaceID INT NOT NULL AUTO_INCREMENT,
    managerID INT NOT NULL,
    suburb VARCHAR(15) NOT NULL,
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

# Sample data
INSERT INTO Payrate (roleName, payRate) VALUES ("Floor Worker", 2.80), 
	("CEO", 100.01),
    ('Window Cleaning', 5.76),
    ('CFO', 82.9),
    ('Shelf Stocker', 14.21),
    ('Store Manager', 30.50);

INSERT INTO Staff (roleName, name, password, isManager)
VALUES ("Floor Worker", "Joe Smith", SHA2("Im not joe smith", 256), False),
("CEO", "Chad Chadwitch", SHA2("yes.itisI", 256), True),
("Store Manager", "Cool Bill", SHA2("eatmy***", 256), True),
("Shelf Stocker", "Hugo Phillips", SHA2("Ilovepeople", 256), False);

INSERT INTO Workplace (managerID, suburb) VALUES (2, 'Indooripilly'), (3, 'Ipswich');  # Chad Chadwitch

INSERT INTO Roster (staffID, date, workplaceID, duration)
VALUES (1, "2021-06-08", 1, 4),  # Joe Smith
(2, "2021-06-09", 1, 10),
(2, "2021-06-10", 1, 8),
(2, "2021-06-11", 1, 4),
(2, "2021-06-12", 1, 6),
(2, "2021-06-13", 1, 9),
(2, "2021-06-14", 2, 11),
(2, "2021-06-15", 1, 2),
(2, "2021-06-16", 1, 5),
(3, "2021-06-14", 2, 9);  # Chad Chadwitch

select * from Staff;
