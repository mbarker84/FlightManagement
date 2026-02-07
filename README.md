# Flight Management

## Dependencies

This project requires Python 3 and the Pandas library, which will need to be installed. To install dependencies with Pip run:

```bash
pip install -r requirements.txt
```

## Running the app

Running the _main.py_ file will create the database tables, import the data and open the user menu. The user can select numerical options.

## Test operations

This section provides some example inputs to test the operations with that will produce helpful results.

### Search a flight

Options 1 and 2 from the menu allow users to search flights from the database by flight status and airport respectively.

#### Searching by status

Select option `1`. Statuses are listed.

```
Enter flight status name or ID
Select the numeric option or status name from the list:
...
```

Type `1` (for flights with 'SCHEDULED' status). Flights are shown that match status.

```
...
Enter the flight ID to view flight schedule (or type X to return to menu):
```

Type Flight ID `14`. The UI shows a flight summary and schedule. This particular flight has two destinations.

#### Searching by airport

From the main menu, select option `2`.

```
Enter 3-letter airport code (or type X to return to menu):
```

Enter `LHR` (upper or lowercase). The UI should list all flights that have the airport code 'LHR' as their departure or final arrival destination. (Flight 14 is NOT shown, which has 'LHR' as an interim destination.)

Repeat the steps above to view a flight.

### Add a flight

Select option `3` from the main menu.

```
Enter Flight Number (must be 4 digits or less) (or type X to return to menu):
```

Enter a new flight number, e.g. `200`. (Flight numbers do not have to be unique.)

```
Enter aeroplane registration code (or type X to return to menu):
```

Enter `N505DL`.

```
Enter departure date in the format YYYY-MM-DD HH:MM (or type X to return to menu)
```

Enter `2026-04-01 09:00`

```
Enter departure airport code (or type X to return to menu):
```

Enter `LHR`.

```
Enter arrival date in the format YYYY-MM-DD HH:MM (or type X to return to menu)
```

Enter `2026-04-01 13:00`.

```
Enter arrival airport code (or type X to return to menu):
```

Enter `BCO`. The UI should show a summary of the newly created flight.

### Delete a flight

Select `4` from the main menu.

```
Enter Flight ID to delete (or type X to return to menu):
```

Enter `1`. The UI should display a flight overview and request confirmation:

```
Confirm deletion of the following flight:
1: LHR 2026-04-01 09:00:00 -> DBV 2026-04-01 13:00:00
```

Enter `Y`. The UI should show confirmation of deletion.

### Update a flight

The Update operation allows the user to modify the departure and arrival dates/times of a flight that already exists. Select `5` from the menu.

```
Enter Flight ID to update (or type X to return to menu):
```

Enter `14`. The UI shows a flight summary.

```
...
Enter the departure airport code of the flight segment you want to amend (or press X to return to the main menu):
```

Select the departure airport code for either of the legs of this flight, e.g. `FLI`. The UI shows the selected leg.

```
...
Enter the new departure date (or leave blank to keep existing date):
```

Enter `2026-05-01 12:00`.

```
Enter the new arrival date (or leave blank to keep existing date):
```

Enter `2026-05-01 18:00`. The UI should show confirmation of the change and a summary of the new departure and arrival times.

### View statistics

Selecting `7` from the menu shows some key statistics about the airline, such as popular destinations.
