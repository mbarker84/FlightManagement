from operations.insert_flight import InsertFlight
from operations.search_flights import SearchFlight
from operations.update_flight import UpdateFlight
from operations.setup_db import SetupDB


# Sets up the database and present the user with a menu to select operations.
def main():
  try:
    # Initialise the database and create tables
    SetupDB()

    # Open user menu
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
