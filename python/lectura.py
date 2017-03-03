import csv
f = open('data/FL_insurance_sample.csv')
csv_f = csv.reader(f)

for row in csv_f:
  print(row)
