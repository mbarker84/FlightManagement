from datetime import datetime

class FlightDestination:
  flight_id = None
  departure_time = None
  arrival_time = None
  departure_airport_code = None
  arrival_airport_code = None

  def set_flight_id(self, value):
    self.flight_id = value

  def set_departure_time(self, value):
    self.departure_time = value

  def set_arrival_time(self, value):
    self.arrival_time = value
  
  def set_departure_airport_code(self, value):
    self.departure_airport_code = value

  def set_arrival_airport_code(self, value):
    self.arrival_airport_code = value

  def get_query_insert(self):
    return '''
            INSERT INTO FlightDestination (FlightID, DepartureTime, ArrivalTime, DepartureAirportCode, ArrivalAirportCode) 
            VALUES (?, ?, ?, ?, ?)
            '''

  # Gets the flight data as a tuple for insertion into table
  def get_tuple(self):
    return (self.flight_id, self.departure_time, self.arrival_time, self.departure_airport_code, self.arrival_airport_code)

