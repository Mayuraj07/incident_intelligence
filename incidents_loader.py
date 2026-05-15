import csv

def load_incidents(filepath):
    with open (filepath, newline= '', encoding='utf-8-sig') as f:
       return list(csv.DictReader(f))
    
incidents = load_incidents('incidents.csv')   


print('Total Incidents:' , len(incidents))

print()

print("First row")
for key, value in incidents[0].items():
    print(f" {key}: {value}")
      
