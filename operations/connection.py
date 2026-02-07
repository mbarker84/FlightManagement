import sqlite3

class DBConnection:
  db_name = 'flight-management.db'

  def __init__(self):
    self.conn = sqlite3.connect(self.db_name)
    self.cur = self.conn.cursor()

  def get_connection(self):
    return self.conn
