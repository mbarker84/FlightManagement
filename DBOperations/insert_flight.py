from datetime import datetime
from Flight import Flight
from FlightDestination import FlightDestination

def insert_flight(cursor):
  flight_details = Flight(int(input('Enter FlightNumber: ')))
  flight_dest = FlightDestination()

  # AeroplaneRegistrationCode must be in Aeroplane table
  while True:
    try:
      aeroplane_id = input('Enter AeroplaneRegistrationCode: ')

      # Check aeroplane ID is in database
      cursor.execute('SELECT RegistrationCode FROM Aeroplane WHERE RegistrationCode = ?', (aeroplane_id.upper(),))
      aeroplane_in_list = cursor.fetchone()

      if aeroplane_in_list:
        flight_details.set_aeroplane_id(aeroplane_id)
        break
      else:
        raise Exception('Aeroplane registration code is not in the database. Please try again.')
    except Exception as e:
      print(e)

  # Validate departure date
  # Allow user to input YYYY-MM-DD HH:MM, but format to YYYY-MM-DD HH:MM for database
  while True:
    try:
      input_date = input('Enter departure date in the format YYYY-MM-DD HH:MM\n')
      datetime.strptime(input_date, '%Y-%m-%d %H:%M')
      flight_dest.set_departure_time(input_date + ':00')
      flight_details.set_departure_date(input_date + ':00')
      break
    except ValueError:
      print('Invalid date')

  # Add flight to database
  cursor.execute(flight_details.get_query_insert(), flight_details.get_tuple())

  # Schedule the flight: add departure and arrival information
  # Get flight ID of the flight we just added
  cursor.execute('SELECT MAX(FlightID) FROM Flight')
  flight_id = cursor.fetchone()

  if flight_id == None:
    raise Exception('Flight ID not found.')
  
  print('Flight ID: ' + flight_id)
  flight_dest.set_flight_id(flight_id)

  # Departure airport code
  while True:
    try:
      airport_code = input('Enter DepartureAirportCode: ')

      # Check airport code is in database
      cursor.execute('SELECT AirportCode FROM Destination WHERE AirportCode = ?', (airport_code,))
      code_in_list = cursor.fetchone()

      if code_in_list:
        flight_dest.set_departure_airport_code(airport_code)
        break
      else:
        raise Exception('Airport code is not in the database. Please try again.')
    except Exception as e:
      print('Airport code is not in the database. Please try again.')

  # Set arrival date/time
  while True:
    try:
      input_date = input('Enter arrival date in the format YYYY-MM-DD HH:MM\n')
      datetime.strptime(input_date, '%Y-%m-%d %H:%M')
      flight_dest.set_arrival_time(input_date + ':00')
      break
    except ValueError:
      print('Invalid date')

  # Set arrival airport
  while True:
    try:
      airport_code = input('Enter arrival airport code: ')

      # Check airport code is in database
      cursor.execute('SELECT AirportCode FROM Airport WHERE AirportCode = ?', (airport_code.upper(),))
      airport_in_list = cursor.fetchone()

      if airport_in_list:
        flight_dest.set_arrival_airport_code(airport_code)
        break
      else:
        raise Exception('Airport code is not in the database. Please try again.')
    except Exception (e):
      print(e)

  # Add flight destination to database
  cursor.execute(flight_dest.get_query_insert(), flight_dest.get_tuple())
  cursor.execute('SELECT * FROM FlightDestination WHERE FlightID = ?', (flight_id,))
  result = cursor.fetchall()

  for item in result:
    print(item)



  