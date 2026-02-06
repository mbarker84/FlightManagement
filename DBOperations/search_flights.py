from DBOperations.connection import DBConnection
from Flight import Flight
from DBOperations.flight_list import FlightList

class SearchFlight:
  selected_flight = None

  # These two queries are almost the same, we are just filtering by a different variable
  sql_get_flight_by_status = '''
                    SELECT Flight.FlightID, 
                    (SELECT FlightDestination.DepartureAirportCode FROM FlightDestination
                    WHERE FlightDestination.FlightID = Flight.FlightID
                    ORDER BY DepartureTime ASC
                    LIMIT 1) AS DepartureAirportCode, 
                    (SELECT FlightDestination.DepartureTime FROM FlightDestination
                    WHERE FlightDestination.FlightID = Flight.FlightID
                    ORDER BY DepartureTime ASC
                    LIMIT 1) AS DepTime, 
                    (SELECT FlightDestination.ArrivalAirportCode FROM FlightDestination
                    WHERE FlightDestination.FlightID = Flight.FlightID
                    ORDER BY DepartureTime DESC
                    LIMIT 1) AS ArrivalAirportCode, 
                    (SELECT FlightDestination.ArrivalTime FROM FlightDestination
                    WHERE FlightDestination.FlightID = Flight.FlightID
                    ORDER BY DepartureTime DESC
                    LIMIT 1) AS ArrivalTime,
                    FlightNumber
                    FROM Flight
                    WHERE StatusID = ?
                    ORDER BY DepTime
                    '''
  
  sql_get_flight_by_airport = '''
                    SELECT Flight.FlightID, 
                    (SELECT FlightDestination.DepartureAirportCode FROM FlightDestination
                    WHERE FlightDestination.FlightID = Flight.FlightID
                    ORDER BY DepartureTime ASC
                    LIMIT 1) AS DepartureAirportCode, 
                    (SELECT FlightDestination.DepartureTime FROM FlightDestination
                    WHERE FlightDestination.FlightID = Flight.FlightID
                    ORDER BY DepartureTime ASC
                    LIMIT 1) AS DepTime, 
                    (SELECT FlightDestination.ArrivalAirportCode FROM FlightDestination
                    WHERE FlightDestination.FlightID = Flight.FlightID
                    ORDER BY DepartureTime DESC
                    LIMIT 1) AS ArrivalAirportCode, 
                    (SELECT FlightDestination.ArrivalTime FROM FlightDestination
                    WHERE FlightDestination.FlightID = Flight.FlightID
                    ORDER BY DepartureTime DESC
                    LIMIT 1) AS ArrivalTime,
                    FlightNumber
                    FROM Flight
                    WHERE DepartureAirportCode = ?
                    OR ArrivalAirportCode = ?
                    ORDER BY DepTime
                    '''

  sql_search_flight_status_name = 'SELECT StatusID FROM FlightStatus WHERE StatusName = ?'
  
  
  def __init__(self, value):
    self.search_option = value

    if value == 1:
      self.search_by_status()
    elif value == 2:
      self.search_by_airport()

  
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
        self.flight_id = input('Enter the flight ID to view flight schedule (or type X to return to menu): ')

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
        
        # Get and print the detailed flight schedule
        flight = FlightList(self.selected_flight)
        flight.print_summary()
        flight.print_flight_schedule()

        break
      except Exception as e:
        print('⚠️ An error occured: ' + str(e))

  
  # Format and print the flight list
  # (Some flights may have multiple stops, so only the final destination is shown)
  def show_flights(self, flights):
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


  def show_flight_statuses(self):
    try:
      self.get_connection()
      self.cur.execute('SELECT StatusID, StatusName, StatusDescription FROM FlightStatus')
      results = self.cur.fetchall()

      print('Select the numeric option or status name from the list:')
      print('--------')
      for item in results:
        print(str(item[0]) + ': ' + item[1] + ' ' + item[2])
      print('--------')

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


  # Search flights by status
  def search_by_status(self):
    while True:
      # status_id = input('Enter flight status name or ID (or type X to return to menu): ')
      print('Enter flight status name or ID')

      # Get flight statuses and descriptions
      self.show_flight_statuses()
      status_id = input('Enter option (or type X to return to menu): ')

      # Return to main menu
      if status_id.upper() == 'X':
        break

      try:
        # Reset flights
        self.flights = []

        # Check if input is integer, if so get the status name from the ID
        status_id = self.check_flight_status_input(status_id)

        # Show an error message if status invalid
        if status_id == None:
          raise Exception('Not a valid flight status. Please try again')
        
        # Select all flights with the corresponding status
        self.get_connection()
        self.cur.execute(self.sql_get_flight_by_status, (status_id,))
        results = self.cur.fetchall()

        if len(results) == 0:
          print('No flights match the criteria.')
          break

        # Print their ID, departure time and airport, arrival time and destination.
        self.show_flights(results)

        # Allow the user to select a flight from the list to view more details
        self.view_flight_details()
        break

      except Exception as e:
        print('⚠️ An error occured: ' + str(e))
      finally:
        self.conn.close()

  # Search flights by airport
  def search_by_airport(self):
    while True:
      airport_id = input('Enter 3-letter airport code (or type X to return to menu): ')

      # Return to main menu
      if airport_id.upper() == 'X':
        break

      try:
        # Reset flights
        self.flights = []

        # Select flights that have the airport ID as departure or arrival destination
        self.get_connection()
        self.cur.execute(self.sql_get_flight_by_airport, (airport_id.upper(), airport_id.upper()))

        results = self.cur.fetchall()

        if len(results) == 0:
          print('No flights match the criteria.')
          break

        # Print their ID, departure time and airport, arrival time and destination.
        self.show_flights(results)

        # Allow the user to select a flight from the list to view more details
        self.view_flight_details()
        break

      except Exception as e:
        print('⚠️ An error occured: ' + str(e))
      finally:
        self.conn.close()