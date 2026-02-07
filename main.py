from operations.connection import DBConnection
from operations.insert_flight import InsertFlight
from operations.import_data import ImportData
from operations.search_flights import SearchFlight
from operations.update_flight import UpdateFlight

# Initialise the database, create tables and import data
class operations:
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


# The user will select a choice from the menu to interact with the database.
def main():
  try:
    operations()

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
      if __choose_menu == 1:
        SearchFlight(1)
      elif __choose_menu == 2:
        SearchFlight(2)
      elif __choose_menu == 3:
        InsertFlight()
      elif __choose_menu == 4:
        UpdateFlight('delete')
      elif __choose_menu == 5:
        UpdateFlight('update')
      elif __choose_menu == 6:
        exit(0)
      else:
        print("Invalid Choice")
  
  except Exception as e:
    print('Exited due to exception: ' + str(e))

if __name__ == '__main__':
  main()
