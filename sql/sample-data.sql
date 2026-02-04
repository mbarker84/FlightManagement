INSERT INTO Aeroplane (RegistrationCode, Capacity, Manufacturer, Model, NoOfPilots, NoOfCrew) VALUES 
  ('G-AAAA', 350, 'Boeing', '747-800', 2, 5),
  ('G-BAAA', 350, 'Boeing', '747-800', 2, 5),
  ('G-CAAA', 350, 'Boeing', '747-800', 2, 5),
  ('G-DAAA', 350, 'Boeing', '747-800', 2, 5),
  ('G-EAAA', 180, 'Boeing', '737-800', 2, 4),
  ('G-FAAA', 180, 'Boeing', '737-800', 2, 4),
  ('G-GAAA', 180, 'Boeing', '737-800', 2, 4),
  ('G-HAAA', 190, 'Boeing', '737-800', 2, 4),
  ('G-IAAA', 360, 'Boeing', '777-300ER', 2, 5),
  ('G-JAAA', 360, 'Boeing', '777-300ER', 2, 5),
  ('G-KAAA', 247, 'Airbus', 'A300', 2, 4),
  ('G-LAAA', 247, 'Airbus', 'A300', 2, 4);

INSERT INTO FlightStatus (StatusName, StatusDescription) VALUES
  ('SCHEDULED', 'Indicates that the flight is scheduled by the carrier.'),
  ('OUT-GATE', 'Aircraft has left the departing gate. Also known as: Chocks off'),
  ('IN-AIR', 'Aircraft has taken off. Also known as: Wheels Up, Airborne'),
  ('LANDED', 'Aircraft has landed. Also known as: Wheels Down, Touchdown'),
  ('IN-GATE', 'Aircraft now at arriving gate. Also known as: Chocks on'),
  ('CANCELLED', 'Flight is now canceled.'),
  ('DIVERTED', 'Flight has been diverted. Note that this status can happen anytime after OutGate and before InGate.'),
  ('PROPOSED', 'Indicates a General Aviation flight is proposed for the route.');

INSERT INTO Person (FirstName, LastName) VALUES
  ('Alan', 'George'),
  ('Sara', 'Rodrigues'),
  ('Milo', 'Smith'),
  ('Iris', 'Wallingford'),
  ('Hector', 'Lewis'),
  ('Marie', 'Granger'),
  ('Elsie', 'Lowe')
;