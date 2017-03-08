import pandas as pd
import json

with open('/home/administradorcito/data-graduates/Introduction_01/data/countries.json') as data_file:
        data = json.load(data_file)

for i in data:
	print(i)                                    
~                 
