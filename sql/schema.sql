DROP TABLE IF EXISTS Flight;
DROP TABLE IF EXISTS FlightStatus;
DROP TABLE IF EXISTS Person;
DROP TABLE IF EXISTS PersonEmail;
DROP TABLE IF EXISTS PersonTelephone;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Aeroplane;
DROP TABLE IF EXISTS Airport;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS PilotAssignment;
DROP TABLE IF EXISTS CrewAssignment;
DROP TABLE IF EXISTS FlightDestination;

CREATE TABLE FlightStatus (
  StatusID INTEGER PRIMARY KEY,
  StatusName TEXT NOT NULL,
  StatusDescription TEXT
);

CREATE TABLE Person (
  PersonID INTEGER PRIMARY KEY,
  FirstName TEXT NOT NULL,
  LastName TEXT NOT NULL
);

CREATE TABLE Employee (
  PersonID INTEGER PRIMARY KEY,
  Position TEXT,
  Pilot BOOLEAN,
  Crew BOOLEAN,
  SALARY INTEGER,
  FOREIGN KEY (PersonID) REFERENCES Person (PersonID)
);

CREATE TABLE PersonEmail (
  EmailAddress TEXT NOT NULL PRIMARY KEY,
  PersonID INTEGER NOT NULL,
  ContactType TEXT,
  FOREIGN KEY (PersonID) REFERENCES Person (PersonID)
);

CREATE TABLE PersonTelephone (
  TelephoneNo TEXT NOT NULL PRIMARY KEY,
  PersonID INTEGER NOT NULL,
  ContactType TEXT,
  FOREIGN KEY (PersonID) REFERENCES Person (PersonID)
);

CREATE TABLE Aeroplane (
  RegistrationCode TEXT NOT NULL PRIMARY KEY,
  Capacity INTEGER NOT NULL,
  Manufacturer TEXT,
  Model TEXT,
  NoOfPilots INTEGER,
  NoOfCrew INTEGER
);

CREATE TABLE Airport (
  AirportCode TEXT NOT NULL PRIMARY KEY,
  AirportName TEXT,
  Country TEXT,
  City TEXT
);

CREATE TABLE Flight (
  FlightID INTEGER PRIMARY KEY,
  FlightNumber INT CHECK (FlightNumber<=4),
  AeroplaneRegistrationCode TEXT NOT NULL,
  DepartureDate DATETIME,
  StatusID INTEGER,
  FOREIGN KEY (StatusID) REFERENCES FlightStatus (StatusID)
);

CREATE TABLE Booking (
  FlightID INTEGER NOT NULL,
  PersonID INTEGER NOT NULL,
  SeatNumber INTEGER,
  PRIMARY KEY (FlightID, PersonID),
  FOREIGN KEY (PersonID) REFERENCES Person (PersonID)
);

CREATE TABLE PilotAssignment (
  FlightID INTEGER NOT NULL,
  PersonID INTEGER NOT NULL,
  PRIMARY KEY (FlightID, PersonID),
  FOREIGN KEY (PersonID) REFERENCES Employee (PersonID)
);

CREATE TABLE CrewAssignment (
  FlightID INTEGER NOT NULL,
  PersonID INTEGER NOT NULL,
  PRIMARY KEY (FlightID, PersonID),
  FOREIGN KEY (PersonID) REFERENCES Employee (PersonID)
);

CREATE TABLE FlightDestination (
  FlightID INTEGER NOT NULL,
  DepartureAirportCode TEXT NOT NULL,
  ArrivalAirportCode TEXT NOT NULL,
  DepartureTime DATETIME,
  ArrivalTime DATETIME,
  PRIMARY KEY (FlightID, DepartureTime, ArrivalTime)
);





