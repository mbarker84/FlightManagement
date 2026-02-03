from datetime import datetime

class Flight:
  flight_id = None
  flight_number = None
  aeroplane_id = None
  departure_date = None

  def __init__(self, id):
    self.flight_number = id

  def get_flight_id(self):
    return self.flight_id
  
  def get_flight_number(self):
    return self.flight_number
  
  def get_departure_date(self):
    return datetime.isoformat(self.departure_date)
  
  def get_aeroplane_id(self):
    return self.aeroplane_id
  
  # Gets the flight data as a tuple for insertion into table
  def get_tuple(self):
    return (self.flight_number, self.aeroplane_id, self.departure_date)

  def set_flight_number(self, id):
    self.flight_number = int(id)

  def set_aeroplane_id(self, id):
    self.aeroplane_id = str(id)

  def set_departure_date(self, id):
    self.departure_date = id

  def __str__(self):
    return str(self.get_flight_id) + "\n" + self.aeroplane_id + "\n" + self.departure_date