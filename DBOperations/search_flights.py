from DBOperations.connection import DBConnection

class SearchFlight:
  sql_search_flight_status_id = 'SELECT StatusName, StatusID FROM FlightStatus WHERE StatusID = ?'
  sql_search_flight_status_name = 'SELECT StatusID FROM FlightStatus WHERE StatusName = ?'
  
  sql_query_status = '''
                    SELECT FlightDestination.FlightID,
                      (SELECT DepartureAirportCode FROM FlightDestination AS fd
                      WHERE fd.FlightID = FlightDestination.FlightID
                      ORDER BY DepartureTime
                      LIMIT 1) AS DepartureAirportCode,
                      ArrivalAirportCode,
                      MIN(DepartureTime) AS DepTime,
                      MAX(ArrivalTime) AS ArrivalTime 
                    FROM FlightDestination
                    WHERE FlightID IN
                       (SELECT FlightID FROM Flight WHERE StatusID = ?)
                    GROUP BY FlightID
                    ORDER BY DepTime
                    '''
  
  # Get database connection
  def get_connection(self):
    self.conn = DBConnection().get_connection()
    self.cur = self.conn.cursor()

  # check input is a valid flight status ID or name
  def check_flight_status_input(self, input_string):
    if input_string.isdigit() == True:
      return int(input_string)
    else:
      try:
        status_name = input_string.upper()
        self.cur.execute(self.sql_search_flight_status_name, (status_name,))
        status = self.cur.fetchone()
        return status[0]
      except:
        return None

  def search_by_status(self):
    while True:
      status_id = input('Enter flight status name or ID (or type X to return to menu): ')

      # Return to main menu
      if status_id.upper() == 'X':
        break

      try:
        self.get_connection()

        # Check if input is integer, if so get the status name from the ID
        status_id = self.check_flight_status_input(status_id)

        if status_id == None:
          raise Exception('Not a valid flight status. Please try again')
        
        # self.cur.execute(self.sql_dep_arr_airports)
        # results = self.cur.fetchall()
        # for row in results:
        #   print(row)

        # break

        self.cur.execute(self.sql_query_status, (status_id,))
        results = self.cur.fetchall()

        if len(results) <= 0:
          print('No flights match the criteria.')

        for row in results:
          print(str(row[0]) + ' ' + row[1] + ' ' + row[3] + ' -> ' + row[2] + ' ' + row[4])

        break

      except Exception as e:
        print('⚠️ An error occured: ' + str(e))
      finally:
        self.conn.close()

