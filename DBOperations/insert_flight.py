from datetime import datetime
from Flight import Flight
from FlightDestination import FlightDestination

def insert_flight(cursor):
  flight_details = Flight(int(input("Enter FlightNumber: ")))
  flight_dest = FlightDestination()

  # AeroplaneRegistrationCode must be in Aeroplane table
  while True:
    try:
      aeroplane_id = input("Enter AeroplaneRegistrationCode: ")

      # Check aeroplane ID is in database
      cursor.execute("SELECT RegistrationCode FROM Aeroplane WHERE RegistrationCode = ?", (aeroplane_id,))
      aeroplane_in_list = cursor.fetchone()

      if aeroplane_in_list:
        flight_details.set_aeroplane_id(aeroplane_id)
        break
      else:
        raise Exception("Aeroplane registration code is not in the database. Please try again.")
    except Exception as e:
      print(e)

  # Validate departure date
  while True:
    try:
      ddate = input("Enter DepartureDate in the format YYYY-MM-DD HH:MM:SS:")
      datetime.strptime(ddate, "%Y-%m-%d %H:%M:%S")
      flight_details.set_departure_date(ddate)
      break
    except ValueError:
      print("Invalid date")

  # Departure airport code
  while True:
    try:
      airport_code = input("Enter DepartureAirportCode: ")

      # Check airport code is in database
      cursor.execute("SELECT AirportCode FROM Destination WHERE AirportCode = ?", (airport_code,))
      code_in_list = cursor.fetchone()

      if code_in_list:
        flight_dest.set_departure_airport_code(airport_code)
        break
      else:
        raise Exception("Airport code is not in the database. Please try again.")
    except Exception as e:
      print("Airport code is not in the database. Please try again.")

  # Insert destination

  # Insert flight
  cursor.execute(flight_details.get_query_insert(), flight_details.get_tuple())