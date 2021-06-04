import json

status_file = open('status.json',)
  
status = json.load(status_file)
status_file.close()

print(status)