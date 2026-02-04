import sqlite3
import pandas as pd
from DBOperations.insert_flight import insert_flight

# Define DBOperation class to manage all data into the database.
class DBOperations:
  db_name = 'flight-management.db'

  # sql_insert = ""
  # sql_select_all = "SELECT * from Flights"
  # sql_search = "SELECT * from Flights where FlightID = ?"
  # sql_alter_data = ""
  # sql_update_data = ""
  # sql_delete_data = ""
  # sql_drop_table = ""

  # Initialise the database, import data and create tables
  def __init__(self):
    self.create_tables()
    self.import_airports()
    self.populate_database()

  # Creates tables from SQL file
  def create_tables(self):
    try:
      self.conn = sqlite3.connect(self.db_name)
      self.cur = self.conn.cursor()

      # Create the database using the SQL file
      with open('sql/schema.sql') as schema:
        sql_create = schema.read().split(";")

      # Execute each SQL statement to create the tables
      for statement in sql_create:
        self.cur.execute(statement)

      self.conn.commit()
      print('✅ Tables created successfully')
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # Import airport data from CSV
  def import_airports(self):
    try:
      self.get_connection()
      airports_data_raw = pd.read_csv('data/airports.csv')

      for index, row in airports_data_raw.iterrows():
        query = '''INSERT INTO Airport (AirportCode, AirportName, Country, City) VALUES(?, ?, ?, ?)'''
        self.cur.execute(query, (row['IATA'], row['Airport name'], row['Country'], row['City']))

      # Check
      self.cur.execute('SELECT * FROM Airport LIMIT 5')
      rows = self.cur.fetchall()

      if (len(rows) == 0):
        raise Exception('Failed to import airport data.')
      else:
        print('✅ Airports imported')

      # for row in rows:
      #   print(row[0] + ' ' + row[1] + ' ' + row[2] + ' ' + row[3])

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # Populates the database with sample data
  def populate_database(self):
    try:
      self.conn = sqlite3.connect(self.db_name)
      self.cur = self.conn.cursor()

      # Create the database using the SQL file
      with open('sql/sample-data.sql') as schema:
        sql_insert = schema.read().split(';')

      # Execute each SQL statement to create the tables
      for statement in sql_insert:
        self.cur.execute(statement)

      self.conn.commit()
      print('✅ Sample data added')
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def get_connection(self):
    self.conn = sqlite3.connect(self.db_name)
    self.cur = self.conn.cursor()

  def check_data(self):
    try:
      self.get_connection()
      result = self.cur.execute("SELECT * FROM Aeroplane")
      result = self.cur.fetchall()

      for item in result:
        print(item)

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def insert_data(self):
    try:
      self.get_connection()

      insert_flight(self.cur)

      # flight_details = Flight(int(input("Enter FlightNumber: ")))
      # flight_dest = FlightDestination()

      # # AeroplaneRegistrationCode must be in Aeroplane table
      # while True:
      #   try:
      #     aeroplane_id = input("Enter AeroplaneRegistrationCode: ")

      #     # Check aeroplane ID is in database
      #     self.cur.execute("SELECT RegistrationCode FROM Aeroplane WHERE RegistrationCode = ?", (aeroplane_id,))
      #     aeroplane_in_list = self.cur.fetchone()

      #     if aeroplane_in_list:
      #       flight_details.set_aeroplane_id(aeroplane_id)
      #       break
      #   except Exception as e:
      #     print("Aeroplane registration code is not in the database. Please try again.")

      # # Validate departure date
      # while True:
      #   try:
      #     ddate = input("Enter DepartureDate in the format YYYY-MM-DD HH:MM:SS:")
      #     datetime.strptime(ddate, "%Y-%m-%d %H:%M:%S")
      #     flight_details.set_departure_date(ddate)
      #     break
      #   except ValueError:
      #     print("Invalid date")

      # # Departure airport code
      # while True:
      #   try:
      #     airport_code = input("Enter DepartureAirportCode: ")

      #     # Check airport code is in database
      #     self.cur.execute("SELECT AirportCode FROM Destination WHERE AirportCode = ?", (airport_code,))
      #     code_in_list = self.cur.fetchone()

      #     if code_in_list:
      #       flight_dest.set_departure_airport_code(airport_code)
      #       break
      #   except Exception as e:
      #     print("Airport code is not in the database. Please try again.")

      # # Insert destination

      # # Insert flight
      # self.cur.execute(flight_details.get_query_insert(), flight_details.get_tuple())

      self.conn.commit()
      print("Inserted data successfully")
    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def select_all(self):
    try:
      self.get_connection()
      # self.cur.execute(self.sql_select_all)
      self.cur.execute("SELECT * FROM Flight")
      result = self.cur.fetchall()

      for item in result:
        print(item)

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def search_data(self):
    try:
      self.get_connection()
      flightID = int(input("Enter FlightNo: "))
      self.cur.execute(self.sql_search, tuple(str(flightID)))

      result = self.cur.fetchone()

      if type(result) == type(tuple()):
        for index, detail in enumerate(result):
          if index == 0:
            print("Flight ID: " + str(detail))
          elif index == 1:
            print("Flight Origin: " + detail)
          elif index == 2:
            print("Flight Destination: " + detail)
          else:
            print("Status: " + str(detail))
      else:
        print("No Record")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  def update_data(self):
    try:
      self.get_connection()

      # Update statement

      if result.rowcount != 0:
        print(str(result.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


# Define Delete_data method to delete data from the table. The user will need to input the flight id to delete the corrosponding record.

  def delete_data(self):
    try:
      self.get_connection()

      if result.rowcount != 0:
        print(str(result.rowcount) + "Row(s) affected.")
      else:
        print("Cannot find this record in the database")

    except Exception as e:
      print(e)
    finally:
      self.conn.close()


# The main function will parse arguments.
# These argument will be definded by the users on the console.
# The user will select a choice from the menu to interact with the database.

db_ops = DBOperations()

while True:
  print("\n Menu:")
  print("**********")
  print(" 1. Check data available")
  print(" 2. Insert data into Flight")
  print(" 3. Select all data from Flight")
  print(" 4. Search a flight")
  print(" 5. Update data some records")
  print(" 6. Delete data some records")
  print(" 7. Exit\n")

  __choose_menu = int(input("Enter your choice: "))
  # db_ops = DBOperations()
  if __choose_menu == 1:
    db_ops.check_data()
  elif __choose_menu == 2:
    db_ops.insert_data()
  elif __choose_menu == 3:
    db_ops.select_all()
  elif __choose_menu == 4:
    db_ops.search_data()
  elif __choose_menu == 5:
    db_ops.update_data()
  elif __choose_menu == 6:
    db_ops.delete_data()
  elif __choose_menu == 7:
    exit(0)
  else:
    print("Invalid Choice")
