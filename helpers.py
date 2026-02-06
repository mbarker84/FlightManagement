from datetime import datetime

def validate_date_input(input_string):
  while True:
    try:
      d = datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")
      break
    except ValueError:
      print("invalid date")
  
  return d


def format_date(input_string):
  while True:
    try:
      d = datetime.strptime(input_string, "%d/%m/%Y %H:%M")
      formatted_date = d.strftime('%Y-%m-%d %H:%M:%S')
      break
    except ValueError:
      print("invalid date")
  
  return formatted_date
  