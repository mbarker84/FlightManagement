from DBOperations.connection import DBConnection
from Flight import Flight
from FlightDestination import FlightDestination

class SearchFlight:
  selected_flight = None

  sql_search_flight_status_id = 'SELECT StatusName, StatusID FROM FlightStatus WHERE StatusID = ?'
  sql_search_flight_status_name = 'SELECT StatusID FROM FlightStatus WHERE StatusName = ?'
  sql_drop_view = 'DROP VIEW IF EXISTS FlightDetails'
  sql_create_view = '''
                    CREATE VIEW FlightDetails AS
                    SELECT FlightDestination.FlightID AS fID,
                      (SELECT DepartureAirportCode FROM FlightDestination AS fd
                      WHERE fd.FlightID = FlightDestination.FlightID
                      ORDER BY DepartureTime
                      LIMIT 1) AS DepartureAirportCode,
                      ArrivalAirportCode,
                      MIN(DepartureTime) AS DepTime,
                      MAX(ArrivalTime) AS ArrivalTime 
                    FROM FlightDestination
                    GROUP BY FlightID
                    ORDER BY DepTime;
                    '''
  
  sql_query_status = '''
                    SELECT fID AS FlightID, DepartureAirportCode, DepTime, ArrivalAirportCode, ArrivalTime,
                      (SELECT FlightNumber FROM Flight AS fl 
                      WHERE fl.FlightID = FlightDetails.fID
                      LIMIT 1) AS FlightNumber
                    FROM FlightDetails
                    WHERE fID IN
                       (SELECT FlightID FROM Flight WHERE StatusID = ?)
                    '''
  
  sql_query_airport = 'SELECT City, AirportCode FROM Airport WHERE AirportCode = ?'
  
  sql_flight_overview = '''
                        SELECT fID AS FlightID,
                          (SELECT City FROM Airport WHERE AirportCode = ?) AS DepartureCity,
                          (SELECT City FROM Airport WHERE AirportCode = ?) AS ArrivalCity
                        FROM FlightDetails
                        WHERE FlightID = ?
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
  
  # Get database connection
  def get_connection(self):
    self.conn = DBConnection().get_connection()
    self.cur = self.conn.cursor()


  # Check input is a valid flight status ID or name
  def check_flight_status_input(self, input_string):
    # If input is number, return as int
    if input_string.isdigit() == True:
      return int(input_string)
    # Otherwise retrieve the ID from the database
    else:
      try:
        status_name = input_string.upper()
        self.cur.execute(self.sql_search_flight_status_name, (status_name,))
        status = self.cur.fetchone()
        return status[0]
      except:
        return None
      

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
      flight = self.selected_flight
      self.cur.execute(self.sql_flight_overview, (flight.get_departure_airport(), flight.get_arrival_airport(), self.flight_id,))
      flight_overview = self.cur.fetchone()

      if flight_overview == None:
        raise Exception('Flight details not found.')
      
      self.selected_flight.set_departure_airport_name(flight_overview[1])
      self.selected_flight.set_arrival_airport_name(flight_overview[2])
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
        self.selected_flight.add_pilot_name(row[0] + ' ' + row[1])
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  
  # Allow the user to select a flight from the list to view more details
  def view_flight_details(self):
    while True:
      try:
        self.flight_id = input('Enter the flight number to view flight schedule (or type X to return to menu): ')

        # Return to main menu
        if str(self.flight_id).upper() == 'X':
          break

        if self.flight_id.isdigit() == False:
          raise Exception('Not a valid flight ID. Must be an integer.')

        self.flight_id = int(self.flight_id)

        # Get flight from list and set as selected flight
        for item in self.flights:
          if item.flight_id == self.flight_id:
            self.selected_flight = item

        if self.selected_flight == None:
          raise Exception('Flight not found.')

        # Get the destinations for the flight
        self.query_flight_destinations()

        # Get overview and pilot details
        self.query_flight_overview()
        self.query_pilot_names()

        # Print flight summary
        print(self.selected_flight.get_summary())

        if self.flight_details == None:
          raise Exception('Unable to retrieve flight details')

        # Print flight schedule
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

        break
      except Exception as e:
        print('⚠️ An error occured: ' + str(e))


  # Search flights by status
  def search_by_status(self):
    while True:
      status_id = input('Enter flight status name or ID (or type X to return to menu): ')

      # Return to main menu
      if status_id.upper() == 'X':
        break

      try:
        self.get_connection()
        self.flights = []

        # Check if input is integer, if so get the status name from the ID
        status_id = self.check_flight_status_input(status_id)

        # Show an error message if status invalid
        if status_id == None:
          raise Exception('Not a valid flight status. Please try again')
        
        # Create view
        self.cur.execute(self.sql_drop_view)
        self.cur.execute(self.sql_create_view)

        # Select flights matching the status ID
        self.cur.execute(self.sql_query_status, (status_id,))
        flights = self.cur.fetchall()

        if len(flights) <= 0:
          raise Exception('No flights match the criteria.')

        self.conn.close()

        # Print their ID, departure time and airport, arrival time and destination.
        # (Some flights may have multiple stops, so only the final destination is shown)
        for row in flights:
          flight = Flight(row[5])
          flight.set_flight_id(row[0])
          flight.set_departure_airport(row[1])
          flight.set_arrival_airport(row[3])
          flight.set_departure_date(row[2])
          flight.set_arrival_date(row[4])
          flight.set_flight_number(row[5])
          self.flights.append(flight)
          print(flight)

        # Allow the user to select a flight from the list to view more details
        self.view_flight_details()
        break

      except Exception as e:
        print('⚠️ An error occured: ' + str(e))
      finally:
        self.conn.close()

