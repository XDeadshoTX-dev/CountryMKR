# -*- coding: cp1251 -*-
import pandas as pd

def test_population_change(file_name):
    data = pd.read_csv(file_name, header=None)
    data.columns = ['Країна', 'Рік', 'Населення']
    data = data.sort_values(['Країна', 'Рік'])
    data['Зміна населення'] = data.groupby('Країна')['Населення'].diff().fillna(0)
    return data

file_name = "population_data.txt"
population_data = test_population_change(file_name)
print(population_data)

