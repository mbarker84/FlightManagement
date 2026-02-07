from operations.connection import DBConnection
from operations.import_data import ImportData

# Initialise the database, create tables and import data
class SetupDB:
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