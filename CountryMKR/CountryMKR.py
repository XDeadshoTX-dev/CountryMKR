# -*- coding: cp1251 -*-
import pandas as pd

def test_population_change(file_name):
    data = pd.read_csv(file_name, header=None)
    data.columns = ['Country', 'Year', 'Population']
    data = data.sort_values(['Country', 'Year'])
    data['Population Change'] = data.groupby('Country')['Population'].diff().fillna(0)
    return data

file_name = "population_data.txt"
population_data = test_population_change(file_name)
print(population_data)
