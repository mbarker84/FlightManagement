from DBOperations.connection import DBConnection
from Flight import Flight

class DeleteFlight:
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

  def __init__(self):
    try:
      self.get_flight()
      self.query_flight()

      # Print the flight
      print('Confirm deletion of the following flight:')
      print(self.flight)

      self.delete_flight()

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
        input_string = input('Enter Flight ID to delete (or type X to return to menu): ')

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

        if input_string != 'Y':
          raise Exception('Invalid input. Enter Y to delete record or X to cancel.')

        self.get_connection()
        
        # Delete records with a relationship to the flight
        self.cur.execute(self.sql_delete_pilot_assignment, (self.flight_id,))
        self.cur.execute(self.sql_delete_flight_destinations, (self.flight_id,))

        # Delete the flight
        self.cur.execute(self.sql_delete_flight, (self.flight_id,))

        print('Flight deleted')
        break

      except Exception as e:
        print('⚠️ ' + str(e))
      finally:
        self.conn.close()