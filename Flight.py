from datetime import datetime

# https://knowledge.oag.com/docs/understanding-flight-status-states

class Flight:
  flight_id = None
  flight_number = None
  aeroplane_id = None
  departure_date = None
  arrival_date = None
  departure_airport = None
  departure_airport_name = None
  arrival_airport = None
  arrival_airport_name = None
  status = 1 # Automatically assigned a status of 'SCHEDULED'
  flight_destination = []
  pilot_name = []

  def __init__(self, flight_number):
    self.flight_number = flight_number

  def get_flight_id(self):
    return self.flight_id
  
  def get_flight_number(self):
    return self.flight_number
  
  def get_query_insert(self):
    return "INSERT INTO Flight (FlightNumber, AeroplaneRegistrationCode, DepartureDate) VALUES (?, ?, ?)"
  
  def get_departure_date(self):
    return self.departure_date
  
  def get_arrival_date(self):
    return self.arrival_date
  
  def get_departure_airport(self):
    return self.departure_airport
  
  def get_arrival_airport(self):
    return self.arrival_airport
  
  def get_aeroplane_id(self):
    return self.aeroplane_id
  
  def get_pilot_names(self):
    return self.pilot_name
  
  def get_status(self):
    return self.status
  
  # Gets the flight data as a tuple for insertion into table
  def get_tuple(self):
    return (self.flight_number, self.aeroplane_id, self.status)
  
  # Get pilot names as string
  def get_pilot_summary(self):
    if len(self.pilot_name) == 0:
      return 'No pilots assigned to this flight'
    
    pilots = ''

    for i in range(len(self.pilot_name)):
      if i < len(self.pilot_name) - 1:
        pilots = pilots + self.pilot_name[i] + ', '
      else:
        pilots = pilots + self.pilot_name[i]
    return 'Pilots: ' + pilots
  
  
  # Flight overview summary
  def get_summary(self):
    return f"""
    Flight {str(self.get_display_id())} from {self.departure_airport_name} to {self.arrival_airport_name}
    {self.get_pilot_summary()}
    """
  
  
  # Flight identifier displayed to customer is a combination of destination and flight number
  def get_display_id(self):
    return f"""{self.arrival_airport}-{str(self.flight_number)}"""
  
  
  # List pilot names as string
  def get_pilot_names(self):
    names = ''

    for name in self.pilot_name:
      names = names + ', ' + name

    return names
  

  def set_flight_number(self, flight_number):
    self.flight_number = int(flight_number)

  def set_flight_id(self, id):
    self.flight_id = int(id)

  def set_aeroplane_id(self, id):
    self.aeroplane_id = str(id)

  def set_departure_date(self, value):
    self.departure_date = value

  def set_arrival_date(self, value):
    self.arrival_date = value

  def set_departure_airport(self, value):
    self.departure_airport = value

  def set_departure_airport_name(self, value):
    self.departure_airport_name = value

  def set_arrival_airport(self, value):
    self.arrival_airport = value

  def set_arrival_airport_name(self, value):
    self.arrival_airport_name = value

  def add_flight_destination(self, dest):
    self.flight_destination.append(dest)

  def set_status(self, value):
    self.status = value

  def remove_flight_destination(self, dest):
    self.flight_destination.remove(dest)

  def add_pilot_name(self, value):
    self.pilot_name.append(value)

  def __str__(self):
    return f"""{str(self.flight_id)} {self.departure_airport} {self.departure_date} -> {self.arrival_airport} {self.arrival_date}"""