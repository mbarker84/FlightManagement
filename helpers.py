from datetime import datetime, date

def validateDateInput(input_string):
  while True:
    try:
      d = datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")
      break
    except ValueError:
      print("invalid date")
  
  return d

def date_adapter(object_date):
    'receives an object_date in the date adapter for adaptation to the new pattern of sqlite3'
    print('Adapter called')
    adapter_format_str = object_date.isoformat()
    return adapter_format_str

def date_conversor(object_bytes):
    'receives an object_bytes from database for the converting in a object_date to python'
    convert_object_str = object_bytes.decode()
    adapter_format_date = datetime.strptime(convert_object_str, '%Y-%m-%d').date()
    return adapter_format_date
  