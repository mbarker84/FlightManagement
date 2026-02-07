from operations.connection import DBConnection
from Flight import Flight
from FlightDestination import FlightDestination
from helpers import validate_date_input

class InsertFlight:
  flight_details = None
  flight_dest = None

  sql_insert_flight = 'INSERT INTO Flight (FlightNumber, AeroplaneRegistrationCode) VALUES (?, ?)'
  sql_insert_destination = '''
          INSERT INTO FlightDestination (FlightID, DepartureAirportCode, ArrivalAirportCode, DepartureTime, ArrivalTime) 
          VALUES (?, ?, ?, ?, ?)'''
  
  sql_select_airport = 'SELECT City FROM Airport WHERE AirportCode = ?'
  
  def __init__(self):
    while True:
      try:
        input_string = input('Enter Flight Number (must be 4 digits or less) (or type X to return to menu): ')

        # Return to main menu
        if str(input_string).upper() == 'X':
          break

        # Check whether input is integer
        if input_string.isdigit() != True:
          raise Exception('Must be an integer')
          
        self.flight_details = Flight(int(input_string))
        self.flight_dest = FlightDestination()

         # User inputs aeroplane code
        self.set_aeroplane_code()

        # Add flight to database so we can get a flight ID
        self.add_flight_to_database()

        # Set the flight ID for the destination so it can be entered into the FlightDestination table
        flight_id = self.flight_details.get_flight_id()
        self.flight_dest.set_flight_id(flight_id)

        self.set_departure_date()
        self.set_departure_airport()
        self.set_arrival_date()
        self.set_arrival_airport()

        # Save the flight destination
        self.save_flight()
        self.print_flight()
        break
      except Exception as e:
        print('⚠️ ' + str(e))


  # Get database connection
  def get_connection(self):
    self.conn = DBConnection().get_connection()
    self.cur = self.conn.cursor()


  # Add flight to database
  def add_flight_to_database(self):
    try:
      self.get_connection()

      flight_number = self.flight_details.get_flight_number()
      aeroplane_code = self.flight_details.get_aeroplane_id()

      self.cur.execute(self.sql_insert_flight, (flight_number, aeroplane_code))
      
      # Get flight ID of the flight we just added
      self.cur.execute('SELECT MAX(FlightID) FROM Flight')
      flight_id = self.cur.fetchone()

      if flight_id == None:
        raise Exception('Flight ID not found.')

      self.flight_details.set_flight_id(flight_id[0])
      print('Flight ' + str(flight_id[0]) + ' added')
    except Exception as e:
      print(e)
    finally:
      self.conn.close()


  # Gets the aeroplane code from user input
  def set_aeroplane_code(self):
    while True:
      try:
        aeroplane_id = input('Enter AeroplaneRegistrationCode (or type X to return to menu): ')

        # Return to main menu
        if str(aeroplane_id).upper() == 'X':
          break

        # Check aeroplane ID is in database
        self.get_connection()
        self.cur.execute('SELECT RegistrationCode FROM Aeroplane WHERE RegistrationCode = ?', (aeroplane_id.upper(),))
        aeroplane_in_list = self.cur.fetchone()

        if aeroplane_in_list:
          self.flight_details.set_aeroplane_id(aeroplane_id[0])
          break
        else:
          raise Exception('Aeroplane registration code is not in the database. Please try again.')
      except Exception as e:
        print(e)
      finally:
        self.conn.close()


  # Validate departure date
  # Allow user to input YYYY-MM-DD HH:MM, but format to YYYY-MM-DD HH:MM for database
  def set_departure_date(self):
    while True:
      try:
        input_date = input('Enter departure date in the format YYYY-MM-DD HH:MM (or type X to return to menu)\n')

        # Return to main menu
        if str(input_date).upper() == 'X':
          break

        validate_date_input(input_date)
        self.flight_dest.set_departure_time(input_date + ':00')
        break
      except ValueError as e:
        print(e)
      except Exception as e:
        print('⚠️ ' + str(e))


  # Get departure airport from user input
  def set_departure_airport(self):
    while True:
      try:
        airport_code = input('Enter departure airport code (or type X to return to menu): ')

        # Return to main menu
        if str(airport_code).upper() == 'X':
          break

        # Check airport code is in database and get airport city name
        self.get_connection()
        self.cur.execute(self.sql_select_airport, (airport_code.upper(),))
        airport_city = self.cur.fetchone()

        if airport_city:
          self.flight_dest.set_departure_airport_code(airport_code.upper())
          self.flight_dest.set_departure_airport_name(airport_city[0])
          break
        else:
          raise Exception('Airport code is not in the database. Please try again.')
      except Exception as e:
        print('⚠️ ' + str(e))
      finally:
        self.conn.close()


  # Set arrival date/time
  def set_arrival_date(self):
    while True:
      try:
        input_date = input('Enter arrival date in the format YYYY-MM-DD HH:MM (or type X to return to menu)\n')

        # Return to main menu
        if str(input_date).upper() == 'X':
          break

        validate_date_input(input_date)
        self.flight_dest.set_arrival_time(input_date + ':00')
        break
      except ValueError as e:
        print(e)
      except Exception as e:
        print('⚠️ ' + str(e))

  
  # Get arrival airport from user input
  def set_arrival_airport(self):
    while True:
      try:
        airport_code = input('Enter arrival airport code (or type X to return to menu): ')

        # Return to main menu
        if str(airport_code).upper() == 'X':
          break

        # Check airport code is in database
        self.get_connection()
        self.cur.execute(self.sql_select_airport, (airport_code.upper(),))
        airport_city = self.cur.fetchone()

        if airport_city:
          self.flight_dest.set_arrival_airport_code(airport_code.upper())
          self.flight_dest.set_arrival_airport_name(airport_city[0])
          break
        else:
          raise Exception('Airport code is not in the database. Please try again.')
      except Exception as e:
        print('⚠️ ' + str(e))
      finally:
        self.conn.close()

  
  # Add flight to database
  def save_flight(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_insert_destination, self.flight_dest.get_tuple())

      print('Flight ' + str(self.flight_details.get_flight_id()) + ' saved')
    except Exception as e:
      raise Exception('Could not save flight: ' + str(e))
    finally:
      self.conn.close()
  

  # Print the saved flight detailss
  def print_flight(self):
    print('---------')
    print('Flight ID: ' + str(self.flight_details.get_flight_id()))
    print('Flight Number: ' + str(self.flight_details.get_flight_number()))
    print('Status: ' + str(self.flight_details.get_status()))
    print(self.flight_dest)
    print('---------')



  