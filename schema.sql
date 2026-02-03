DROP TABLE IF EXISTS Flight;
DROP TABLE IF EXISTS Passenger;
DROP TABLE IF EXISTS Employee;
DROP TABLE IF EXISTS Aeroplane;
DROP TABLE IF EXISTS Destination;
DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS PilotAssignment;
DROP TABLE IF EXISTS CrewAssignment;
DROP TABLE IF EXISTS FlightDestination;

CREATE TABLE Flight (
  FlightID INTEGER PRIMARY KEY,
  FlightNumber INT CHECK (FlightNumber<=4),
  AeroplaneRegistrationCode TEXT NOT NULL,
  DepartureDate DATETIME
);

CREATE TABLE Passenger (
  PassengerID INTEGER PRIMARY KEY,
  FirstName TEXT NOT NULL,
  LastName TEXT NOT NULL
);

CREATE TABLE Employee (
  EmployeeID INTEGER PRIMARY KEY,
  FirstName TEXT NOT NULL,
  LastName TEXT NOT NULL,
  Position TEXT,
  Pilot BOOLEAN,
  Crew BOOLEAN
);

CREATE TABLE Aeroplane (
  RegistrationCode TEXT NOT NULL PRIMARY KEY,
  Capacity INTEGER NOT NULL,
  Manufacturer TEXT,
  Model TEXT,
  NoOfPilots INTEGER,
  NoOfCrew INTEGER
);

CREATE TABLE Destination (
  AirportCode TEXT NOT NULL PRIMARY KEY,
  Capacity INTEGER NOT NULL,
  Manufacturer TEXT,
  Model TEXT,
  NoOfPilots INTEGER,
  NoOfCrew INTEGER
);

CREATE TABLE Booking (
  FlightID INTEGER NOT NULL,
  PassengerID INTEGER NOT NULL,
  SeatNumber INTEGER,
  PRIMARY KEY (FlightID, PassengerID)
);

CREATE TABLE PilotAssignment (
  FlightID INTEGER NOT NULL,
  EmployeeID INTEGER NOT NULL,
  PRIMARY KEY (FlightID, EmployeeID)
);

CREATE TABLE CrewAssignment (
  FlightID INTEGER NOT NULL,
  EmployeeID INTEGER NOT NULL,
  PRIMARY KEY (FlightID, EmployeeID)
);

CREATE TABLE FlightDestination (
  FlightID INTEGER NOT NULL,
  DepartureAirportCode TEXT NOT NULL,
  ArrivalAirportCode TEXT NOT NULL,
  DepartureTime DATETIME,
  ArrivalTime DATETIME,
  PRIMARY KEY (FlightID, DepartureAirportCode, ArrivalAirportCode, DepartureTime, ArrivalTime)
);



