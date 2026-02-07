from operations.connection import DBConnection
from operations.flight_list import FlightList
from Flight import Flight
from FlightDestination import FlightDestination
from helpers import validate_date_input

class UpdateFlight:
  flight_dest = None

  sql_get_flight = '''
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
                    WHERE FlightID = ?
                    '''
  
  sql_delete_flight_destinations = 'DELETE FROM FlightDestination WHERE FlightID = ?'
  sql_delete_flight = 'DELETE FROM Flight WHERE FlightID = ?'
  sql_delete_pilot_assignment = 'DELETE FROM PilotAssignment WHERE FlightID = ?'

  sql_get_destination = '''
                        SELECT DepartureAirportCode, DepartureTime, ArrivalAirportCode, ArrivalTime,
                        (SELECT City FROM Airport 
                          WHERE Airport.AirportCode = FlightDestination.DepartureAirportCode) AS DepartureCity,
                          (SELECT City FROM Airport 
                          WHERE Airport.AirportCode = FlightDestination.ArrivalAirportCode) AS ArrivalCity
                        FROM FlightDestination
                        WHERE FlightID = ?
                        AND DepartureAirportCode = ?
                        '''
  sql_update = '''
                UPDATE FlightDestination 
                SET DepartureTime = ?, ArrivalTime = ?
                WHERE FlightID = ? AND DepartureAirportCode = ?
                '''

  def __init__(self, value):
    try:
      self.query = value
      self.get_flight()
      self.query_flight()

      # Print the flight
      if self.query == 'delete':
        print('Confirm deletion of the following flight:')
        print(self.flight)
        self.delete_flight()
      else:
        print('Update the following flight:')
        print(self.flight)
        self.update_flight()

    except Exception as e:
      print('⚠️ ' + str(e))


  # Get database connection
  def get_connection(self):
    self.conn = DBConnection().get_connection()
    self.cur = self.conn.cursor()


  # Get flight ID from input
  def get_flight(self):
    while True:
      try:
        input_string = input('Enter Flight ID to ' + self.query + ' (or type X to return to menu): ')

        # Return to main menu
        if str(input_string).upper() == 'X':
          break

        self.flight_id = int(input_string)
        break
      except Exception as e:
        print('⚠️ ' + str(e))


  # Get flight details from the database
  def query_flight(self):
    try:
      self.get_connection()
      self.cur.execute(self.sql_get_flight, (self.flight_id,))
      result = self.cur.fetchone()

      self.flight = Flight(result[5])
      self.flight.set_flight_id(result[0])
      self.flight.set_departure_airport(result[1])
      self.flight.set_arrival_airport(result[3])
      self.flight.set_departure_date(result[2])
      self.flight.set_arrival_date(result[4])
      self.flight.set_flight_number(result[5])

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


  def delete_flight(self):
    while True:
      try:
        input_string = input('Press Y to confirm or X to cancel and return to main menu: ')

        # Return to main menu
        if input_string.upper() == 'X':
          break

        if input_string.upper() != 'Y':
          raise Exception('Invalid input. Enter Y to delete record or X to cancel.')

        self.get_connection()
        
        # Delete records with a relationship to the flight
        self.cur.execute(self.sql_delete_pilot_assignment, (self.flight_id,))
        self.cur.execute(self.sql_delete_flight_destinations, (self.flight_id,))

        # Delete the flight
        self.cur.execute(self.sql_delete_flight, (self.flight_id,))

        print('✅ Flight ' + str(self.flight_id) + ' deleted')
        break

      except Exception as e:
        print('⚠️ ' + str(e))
      finally:
        self.conn.close()

  
  # Helper to compare current and edited dates to see if they are different
  def compare_date(self, prev_value, input_string):
    try:
      if len(input_string) == 0:
        new_time = prev_value
      elif input_string != prev_value:
        validate_date_input(input_string)
        new_time = input_string
      else:
        new_time = prev_value
      
      return new_time
    except:
      return None


  # Get new departure date
  def get_new_departure_date(self):
    while True:
      try:
        input_string = input('Enter the new departure date (or leave blank to keep existing date): ')

        new_time = self.compare_date(self.flight_dest.get_departure_time(), input_string)

        if new_time == None:
          raise Exception('Invalid date. Must be in the format YYYY-MM-DD HH:MM')
        
        self.flight_dest.set_departure_time(new_time)
        
        break
      except Exception as e:
        print(e)


  # Get new arrival date
  def get_new_arrival_date(self):
    while True:
      try:
        input_string = input('Enter the new arrival date (or leave blank to keep existing date): ')

        new_time = self.compare_date(self.flight_dest.get_arrival_time(), input_string)

        if new_time == None:
          raise Exception('Invalid date. Must be in the format YYYY-MM-DD HH:MM')
        
        # Do not allow arrival before departure
        if input_string <= self.flight_dest.get_departure_time():
          raise Exception('Arrival date cannot be before departure.')
        
        self.flight_dest.set_arrival_time(new_time)
        
        break
      except ValueError as e:
        print(e)
      except Exception as e:
        print(e)


  def select_destination(self):
    while True:
      try:
        input_string = input('Enter the departure airport code of the flight segment you want to amend (or press X to return to the main menu): ')

        # Return to main menu
        if input_string.upper() == 'X':
          break

        if len(input_string) != 3:
          raise Exception('Not a valid airport code')

        try:
          airport_code = input_string.upper()
        except:
          raise Exception('Not a valid airport code')
        
        
        dest = self.flight.get_dest_details(airport_code)

        if dest == None:
          raise Exception('No flight segment with this airport code')

        # Set and print the selected destination
        self.flight_dest = FlightDestination()
        self.flight_dest.set_departure_airport_code(dest[1])
        self.flight_dest.set_arrival_airport_code(dest[3])
        self.flight_dest.set_departure_time(dest[2])
        self.flight_dest.set_arrival_time(dest[4])
        self.flight_dest.set_departure_airport_name(dest[6])
        self.flight_dest.set_arrival_airport_name(dest[7])

        print(self.flight_dest)
        break

      except Exception as e:
        print('⚠️ ' + str(e))


  # Set new values in database
  def update_database(self):
    try:
      self.get_connection()

      dep_time = self.flight_dest.get_departure_time()
      arr_time = self.flight_dest.get_arrival_time()
      airport_code = self.flight_dest.get_departure_airport_code()

      self.cur.execute(self.sql_update, (self.flight.get_flight_id(), dep_time, arr_time, airport_code))

      # Print the updated flight
      print('✅ Flight destination information updated')
      print(self.flight_dest)

    except Exception as e:
      print('⚠️ ' + str(e))
    finally:
        self.conn.close()


  def print_flight(self):
    self.flight.print_summary()
    self.flight.print_flight_schedule()


  # Update flight times
  def update_flight(self):
    while True:
      try:
        self.flight = FlightList(self.flight)

        # Print the selected flight
        self.print_flight()

        # Select the destination and new values from user input
        self.select_destination()

        if self.flight_dest == None:
          break

        self.get_new_departure_date()

        if self.flight_dest.get_departure_time() == None:
          break

        self.get_new_arrival_date()

        if self.flight_dest.get_arrival_time() == None:
          break

        self.update_database()
        break
      except Exception as e:
        print('⚠️ ' + str(e))