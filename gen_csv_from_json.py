"" write a python script to generate a csv file from json input file  
import csv
import json

def generate_csv(json_file):
  data = []
  with open(json_file) as f:
    data = json.load(f)
  
  keys = data[0].keys()

  with open('output.csv', 'w') as outfile:
    writer = csv.DictWriter(outfile, keys)
    writer.writeheader()
    writer.writerows(data)

generate_csv('data.json')
