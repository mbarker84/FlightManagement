import sqlite3
import pandas as pd
from DBOperations.insert_flight import insert_flight
from DBOperations.import_data import ImportData

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

    # Import data
    importer = ImportData()
    importer.import_all()

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

  # View all scheduled flights
  def view_scheduled_flights(self):
    try:
      self.get_connection()

      query = '''
              SELECT * FROM Flight 
              WHERE StatusID IN 
                (SELECT StatusID FROM FlightStatus WHERE StatusName = ?)
              '''
      self.cur.execute(query, ('SCHEDULED', ))
      rows = self.cur.fetchall()

      for row in rows:
        print(row)

    except Exception as e:
      print(e)
    finally:
      self.conn.close()

  # Insert flight data
  def insert_data(self):
    try:
      self.get_connection()
      insert_flight(self.cur)
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
def main():
  try:
    db_ops = DBOperations()

    while True:
      print("\n Menu:")
      print("**********")
      print(" 1. View scheduled flights")
      print(" 2. Schedule a new flight")
      print(" 3. Select all data from Flight")
      print(" 4. Search a flight")
      print(" 5. Update data some records")
      print(" 6. Delete data some records")
      print(" 7. Exit\n")

      __choose_menu = int(input("Enter your choice: "))
      # db_ops = DBOperations()
      if __choose_menu == 1:
        db_ops.view_scheduled_flights()
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
  
  except Exception as e:
    print('Exited due to exception: ' + str(e))

if __name__ == '__main__':
  main()
