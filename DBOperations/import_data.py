import sqlite3
import pandas as pd

class ImportData():
  db_name = 'flight-management.db'

  sql_insert_airports = 'INSERT INTO Airport (AirportCode, AirportName, Country, City) VALUES(?, ?, ?, ?)'
  sql_insert_people = 'INSERT INTO Person (FirstName, LastName) VALUES(?, ?)'
  sql_insert_aeroplanes = '''
                          INSERT INTO Aeroplane (RegistrationCode, Capacity, Manufacturer, Model, NoOfPilots, NoOfCrew) 
                          VALUES(?, ?, ?, ?, ?, ?)
                          '''
  sql_insert_flights = 'INSERT INTO Flight (FlightNumber, AeroplaneRegistrationCode, StatusID) VALUES(?, ?, ?)'
  sql_insert_flight_status = 'INSERT INTO FlightStatus (StatusName, StatusDescription) VALUES(?, ?)'
  sql_insert_employees = 'INSERT INTO Employee (Position, Pilot, Crew, Salary) VALUES(?, ?, ?, ?)'
  sql_insert_email = 'INSERT INTO PersonEmail (EmailAddress, PersonID, ContactType) VALUES(?, ?, ?)'
  sql_insert_phone = 'INSERT INTO PersonTelephone (TelephoneNo, PersonID, ContactType) VALUES(?, ?, ?)'

  def __init__(self):
    print('Importing data...')

  # Get the database connection
  def get_connection(self):
    self.conn = sqlite3.connect(self.db_name)
    self.cur = self.conn.cursor()

  # Import all data into database
  def import_all(self):
    try:
      self.import_aeroplanes()
      self.import_people()
      self.import_flights()
      self.import_flight_status()
      self.import_people()
      self.import_employees()
      self.import_emails()
      self.import_phone_nos()
    except:
      raise Exception('Error importing data.')

  # Import airport data from CSV
  def import_airports(self):
    try:
      self.get_connection()
      data = pd.read_csv('data/airports.csv')

      for index, row in data.iterrows():
        self.cur.execute(self.sql_insert_airports, (row['IATA'], row['Airport name'], row['Country'], row['City']))

      # Check
      self.cur.execute('SELECT * FROM Airport LIMIT 5')
      rows = self.cur.fetchall()

      if (len(rows) == 0):
        raise Exception('No data added')
      else:
        self.conn.commit()
        print('✅ Airports imported')
        
    except Exception as e:
      print('⚠️ Failed to import airport data.' + str(e))
      raise Exception(e)
    finally:
      self.conn.close()

  # Import people data from CSV
  def import_people(self):
    try:
      self.get_connection()
      data = pd.read_csv('data/people.csv')

      for index, row in data.iterrows():
        self.cur.execute(self.sql_insert_people, (row['FirstName'], row['LastName']))

      # Check
      self.cur.execute('SELECT * FROM Person LIMIT 5')
      rows = self.cur.fetchall()

      if (len(rows) == 0):
        raise Exception('No data added')
      else:
        self.conn.commit()
        print('✅ People imported')
      
    except Exception as e:
      print('⚠️ Failed to import people data.\n' + str(e))
      raise Exception(e)
    finally:
      self.conn.close()

  # Import aeroplane data from CSV
  def import_aeroplanes(self):
    try:
      self.get_connection()
      data = pd.read_csv('data/aeroplanes.csv')

      for index, row in data.iterrows():
        self.cur.execute(self.sql_insert_aeroplanes, (row['RegistrationCode'], row['Capacity'], row['Manufacturer'], row['Model'], 2, row['CrewCapacity']))

      # Check
      self.cur.execute('SELECT * FROM Aeroplane LIMIT 5')
      rows = self.cur.fetchall()

      if (len(rows) == 0):
        raise Exception('No data added')
      else:
        self.conn.commit()
        print('✅ Aeroplanes imported')
        
    except Exception as e:
      print('⚠️ Failed to import aeroplane data.\n' + str(e))
      raise Exception(e)
    finally:
      self.conn.close()

  # Import flight data from CSV
  def import_flights(self):
    try:
      self.get_connection()
      data = pd.read_csv('data/flights.csv')

      for index, row in data.iterrows():
        self.cur.execute(self.sql_insert_flights, (row['FlightNumber'], row['AeroplaneRegistrationCode'], row['StatusID']))

      # Check
      self.cur.execute('SELECT * FROM Flight LIMIT 5')
      rows = self.cur.fetchall()

      if (len(rows) == 0):
        raise Exception('⚠️ Failed to import flight data.')
      else:
        self.conn.commit()
        print('✅ Flights imported')
        
    except Exception as e:
      print('⚠️ Failed to import flight data.\n' + str(e))
      raise Exception(e)
    finally:
      self.conn.close()

  # Import flight status data from CSV
  def import_flight_status(self):
    try:
      self.get_connection()
      data = pd.read_csv('data/flight-status.csv')

      for index, row in data.iterrows():
        self.cur.execute(self.sql_insert_flight_status, (row['StatusName'], row['Description']))

      # Check
      self.cur.execute('SELECT * FROM FlightStatus')
      rows = self.cur.fetchall()

      if (len(rows) == 0):
        raise Exception('No data added')
      else:
        self.conn.commit()
        print('✅ Flights imported')
        
    except Exception as e:
      print('⚠️ Failed to import flight status data.\n' + str(e))
      raise Exception(e)
    finally:
      self.conn.close()

  # Import employee data from CSV
  def import_employees(self):
    try:
      self.get_connection()
      data = pd.read_csv('data/employees.csv')

      for index, row in data.iterrows():
        self.cur.execute(self.sql_insert_employees, (row['Position'], row['Pilot'], row['Crew'], row['Salary']))

      # Check
      self.cur.execute('SELECT * FROM Employee')
      rows = self.cur.fetchall()

      if (len(rows) == 0):
        raise Exception('No data added')
      else:
        self.conn.commit()
        print('✅ Employees imported')
        
    except Exception as e:
      print('⚠️ Failed to import employee data.\n' + str(e))
      raise Exception(e)
    finally:
      self.conn.close()

  # Import email data from CSV
  def import_emails(self):
    try:
      self.get_connection()
      data = pd.read_csv('data/person-email.csv')

      for index, row in data.iterrows():
        self.cur.execute(self.sql_insert_email, (row['Email'], row['PersonID'], row['ContactType']))

      # Check
      self.cur.execute('SELECT * FROM PersonEmail')
      rows = self.cur.fetchall()

      if (len(rows) == 0):
        raise Exception('No data imported.')
      else:
        self.conn.commit()
        print('✅ Email addresses imported')
        
    except Exception as e:
      print('⚠️ Failed to import email data.\n' + str(e))
      raise Exception(e)
    finally:
      self.conn.close()

  # Import phone data from CSV
  def import_phone_nos(self):
    try:
      self.get_connection()
      data = pd.read_csv('data/person-telephone.csv')

      for index, row in data.iterrows():
        self.cur.execute(self.sql_insert_phone, (row['TelephoneNo'], row['PersonID'], row['ContactType']))

      # Check
      self.cur.execute('SELECT * FROM PersonTelephone')
      rows = self.cur.fetchall()

      if (len(rows) == 0):
        raise Exception('No data imported.')
      else:
        self.conn.commit()
        print('✅ Phone numbers imported')
        
    except Exception as e:
      print('⚠️ Failed to import phone data.\n' + e)
    finally:
      self.conn.close()