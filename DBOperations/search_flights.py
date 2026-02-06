from DBOperations.connection import DBConnection
from Flight import Flight
from FlightDestination import Flight

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
  
  sql_query_dep_airport = '''
                          SELECT City, AirportCode FROM Airport
                          WHERE AirportCode IN
                            (SELECT DepartureAirportCode FROM FlightDetails WHERE fID = ?)
                          '''
  
  sql_flight_details = '''
                        SELECT fID AS FlightID, DepartureAirportCode, DepTime, ArrivalAirportCode, ArrivalTime,
                          (SELECT FlightNumber FROM Flight AS fl 
                          WHERE fl.FlightID = FlightDetails.fID
                          LIMIT 1) AS FlightNumber,
                          (SELECT City FROM Airport WHERE AirportCode = ?) AS DepartureCity,
                          (SELECT City FROM Airport WHERE AirportCode = ?) AS ArrivalCity,
                          (SELECT FirstName FROM Person 
                          WHERE PersonID IN
                            (SELECT PersonID FROM PilotAssignment 
                            WHERE PilotAssignment.FlightID = FlightID)) AS PilotFirstName
                        FROM FlightDetails
                        WHERE FlightID = ?
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

        self.cur.execute('SELECT * FROM FlightDestination WHERE FlightID = ?', (self.flight_id, ))
        self.flight_details = self.cur.fetchall()

        if self.flight_details == None or len(self.flight_details) == 0:
          raise Exception('Flight not found.')
        
        # Get flight from list
        for item in self.flights:
          if item.flight_id == int(self.flight_id):
            self.selected_flight = item

        if self.selected_flight == None:
          raise Exception('Something went wrong. Flight not found.')
        
        flight = self.selected_flight

        # Get airport and pilot details for flight
        self.cur.execute(self.sql_flight_details, (flight.get_departure_airport(), flight.get_arrival_airport(), self.flight_id,))
        overview = self.cur.fetchone()

        if overview == None:
          raise Exception('Flight details not found.')

        # Print overview and pilot details
        print(overview)
        
        self.cur.execute(self.sql_query_airport, (flight.get_arrival_airport(),))
        self.arrival_airport = self.cur.fetchone()

        if self.arrival_airport == None:
          raise Exception('Airport not found.')

        print('Flight ' + str(self.flight_id) + ' to ' + self.arrival_airport[0])

        # Print flight schedule
        print('--------' + 'Schedule:')
        for row in self.flight_details:
          print(row)

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
          print('No flights match the criteria.')

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

