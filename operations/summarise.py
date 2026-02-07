from operations.connection import DBConnection

class Summarise:
  sql_query_total_flights = '''SELECT COUNT(*) FROM Flight'''
  
  sql_query_popular_dest = '''SELECT DepartureAirportCode, COUNT(*) AS Total,
                              (SELECT AirportName FROM Airport
                              WHERE Airport.AirportCode = FlightDestination.DepartureAirportCode) AS AirportName,
                              (SELECT City FROM Airport
                              WHERE Airport.AirportCode = FlightDestination.DepartureAirportCode) AS City
                              FROM FlightDestination
                              GROUP BY DepartureAirportCode
                              ORDER BY Total DESC
                              LIMIT 5'''
  
  sql_query_popular_arr = '''SELECT ArrivalAirportCode, COUNT(*) AS Total,
                              (SELECT AirportName FROM Airport
                              WHERE Airport.AirportCode = FlightDestination.ArrivalAirportCode) AS AirportName,
                              (SELECT City FROM Airport
                              WHERE Airport.AirportCode = FlightDestination.ArrivalAirportCode) AS City
                              FROM FlightDestination
                              GROUP BY ArrivalAirportCode
                              ORDER BY Total DESC
                              LIMIT 5'''
  

  def __init__(self):
    try:
      self.get_connection()

      # Get total flights
      self.cur.execute(self.sql_query_total_flights)
      total_flights = self.cur.fetchone()
      print('------------------------------------------------')
      print('⭐️⭐️⭐️⭐️⭐️ ' + str(total_flights[0]) + ' flights served ⭐️⭐️⭐️⭐️⭐️')
      print('------------------------------------------------')

      # Get most popular departure airports
      self.cur.execute(self.sql_query_popular_dest)
      self.dep_airports = self.cur.fetchall()

      # Print results
      print('🛫 Most popular departure airports:')
      self.print_details(self.dep_airports)

      # Get most popular arrival airports
      self.cur.execute(self.sql_query_popular_arr)
      self.arr_airports = self.cur.fetchall()

      # Print results
      print('🛬 Most popular arrival airports:')
      self.print_details(self.arr_airports)
    except:
      raise Exception('Could not retrieve stats.')
    finally:
      self.conn.close()


  # Get database connection
  def get_connection(self):
    self.conn = DBConnection().get_connection()
    self.cur = self.conn.cursor()


  # Print popular destinations
  def print_details(self, results):
    print('------------------------------------------------')
    for row in results:
      total = row[1]
      name = row[2]
      city = row[3]
      print(str(total) + ' flights: ' + name + ', ' + city)
    print('------------------------------------------------')

  