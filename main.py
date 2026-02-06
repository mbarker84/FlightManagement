from DBOperations.connection import DBConnection
from DBOperations.insert_flight import InsertFlight
from DBOperations.import_data import ImportData
from DBOperations.search_flights import SearchFlight

# Define DBOperation class to manage all data into the database.
class DBOperations:
  # Initialise the database, import data and create tables
  def __init__(self):
    self.create_tables()
    self.import_data()

  # Get database connection
  def get_connection(self):
    self.conn = DBConnection().get_connection()
    self.cur = self.conn.cursor()

  # Creates tables from SQL file
  def create_tables(self):
    try:
      self.get_connection()

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

  # Import data from CSVs
  def import_data(self):
    importer = ImportData()
    importer.import_all()

  # View all scheduled flights, their departure dates and destinations
  def view_scheduled_flights(self):
    search = SearchFlight()
    search.search_by_status()


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
      print(" 1. Search flights by status")
      print(" 2. Search flights by airport")
      print(" 3. Schedule a new flight")
      print(" 4. Delete a flight")
      print(" 5. Update a flight")
      print(" 6. Exit\n")

      __choose_menu = int(input("Enter your choice: "))
      # db_ops = DBOperations()
      if __choose_menu == 1:
        SearchFlight(1)
      elif __choose_menu == 2:
        SearchFlight(2)
      elif __choose_menu == 3:
        InsertFlight()
      elif __choose_menu == 4:
        db_ops.search_data()
      elif __choose_menu == 5:
        db_ops.update_data()
      elif __choose_menu == 6:
        exit(0)
      else:
        print("Invalid Choice")
  
  except Exception as e:
    print('Exited due to exception: ' + str(e))

if __name__ == '__main__':
  main()
