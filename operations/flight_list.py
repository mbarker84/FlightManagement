from FlightDestination import FlightDestination
from operations.connection import DBConnection

class FlightList:
  sql_flight_overview = '''
                        SELECT
                        (SELECT City FROM Airport WHERE AirportCode = ?) AS DepartureCity,
                        (SELECT City FROM Airport WHERE AirportCode = ?) AS ArrivalCity
                        FROM Airport
                        '''
  
  sql_flight_dest_details = '''
                        SELECT FlightID, DepartureAirportCode, 
                          DepartureTime, ArrivalAirportCode, ArrivalTime,
                          (SELECT FlightNumber FROM Flight 
                          WHERE Flight.FlightID = FlightDestination.FlightID
                          LIMIT 1) AS FlightNumber,
                          (SELECT City FROM Airport 
                          WHERE Airport.AirportCode = FlightDestination.DepartureAirportCode) AS DepartureCity,
                          (SELECT City FROM Airport 
                          WHERE Airport.AirportCode = FlightDestination.ArrivalAirportCode) AS ArrivalCity
                        FROM FlightDestination
                        WHERE FlightID = ?
                        '''
  
  sql_pilot_names = '''
                    SELECT FirstName, LastName FROM Person
                    WHERE PersonID IN
                      (SELECT PersonID FROM PilotAssignment
                      WHERE PilotAssignment.FlightID = ?)
                    '''
  

  def __init__(self, flight):
    try:
      self.flight = flight
      self.flight_id = self.flight.get_flight_id()

      # Get the destinations for the flight
      self.query_flight_destinations()

      # Get overview and pilot details
      self.query_flight_overview()
      self.query_pilot_names()

      if self.flight_details == None:
        raise Exception('Unable to retrieve flight details')

    except Exception as e:
      print('⚠️ An error occured: ' + str(e))


  def get_flight_id(self):
    return self.flight_id


  # Get database connection
  def get_connection(self):
    self.conn = DBConnection().get_connection()
    self.cur = self.conn.cursor()


  # Get the destinations that correspond to the flight (a flight may have more than one destination)    
  def query_flight_destinations(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_flight_dest_details, (self.flight_id, ))
      self.flight_details = self.cur.fetchall()

      if self.flight_details == None or len(self.flight_details) == 0:
        raise Exception('Flight details not found.')
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  
  # Get the airport details for flight
  def query_flight_overview(self):
    try: 
      self.get_connection()
      self.cur.execute(self.sql_flight_overview, (self.flight.get_departure_airport(), self.flight.get_arrival_airport()))
      flight_overview = self.cur.fetchone()

      if flight_overview == None:
        raise Exception('Flight details not found.')
      
      self.flight.set_departure_airport_name(flight_overview[0])
      self.flight.set_arrival_airport_name(flight_overview[1])
    except Exception as e:
      print(e)
    finally:
      self.conn.close()


  # Get pilots for flight
  def query_pilot_names(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_pilot_names, (self.flight_id, ))
      self.pilots = self.cur.fetchall()

      if self.pilots == None or len(self.pilots) == 0:
        raise Exception('No pilots assigned to selected flight.')
      
      for row in self.pilots:
        self.flight.add_pilot_name(row[0] + ' ' + row[1])
    except Exception as e:
      print(e)
    finally:
      self.conn.close()


  # Print flight schedule
  def print_flight_schedule(self):
    print('--------\n' + 'Schedule:')
    for row in self.flight_details:
      dest = FlightDestination()
      dest.set_departure_airport_code(row[1])
      dest.set_arrival_airport_code(row[3])
      dest.set_departure_time(row[2])
      dest.set_arrival_time(row[4])
      dest.set_departure_airport_name(row[6])
      dest.set_arrival_airport_name(row[7])
      print(dest)
    print('--------')


  # Print flight summary
  def print_summary(self):
    print(self.flight.get_summary())


  # Get the flight segment that matches the departure code
  def get_dest_details(self, dep_airport):
    flight_dest = None

    for row in self.flight_details:
      if row[1] == dep_airport:
        flight_dest = row

    return flight_dest