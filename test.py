import sqlite3

# Connect database
conn = sqlite3.connect('store.db')

print('Database created')

conn.execute('DROP TABLE IF EXISTS Pet')

#Create table
conn.execute('''CREATE TABLE Pet (
              id INT PRIMARY KEY,
              name VARCHAR(20),
              owner VARCHAR(20),
              species VARCHAR(20),
              sex CHAR(1),
              checkups SMALLINT UNSIGNED,
              birth DATE,
              death DATE
             );''')

print('Table created')

# Insert rows
conn.execute('''INSERT INTO Pet (name, owner, species, sex, checkups, birth, death) VALUES 
             ('Fluffy', 'Bob', 'cat', 'f', 6, '2025-01-01', ''),
             ('Al', 'Camilla', 'dog', 'm', 2, '2020-11-03', '2026-01-01')
             ''')

print("Total number of rows created :", conn.total_changes)

rows = conn.execute('SELECT * FROM Pet')

for row in rows:
  print(row)

conn.execute('''UPDATE Pet
             SET death = '2026-01-01'
             WHERE name = 'Fluffy'
             ''')

rows = conn.execute('''SELECT * FROM Pet WHERE name = "Fluffy"''')

print('Updated rows:')
for row in rows:
  print(row)

# Close connection
conn.close()


