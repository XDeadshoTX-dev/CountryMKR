# -*- coding: cp1251 -*-
import pandas as pd

def test_population_change(file_name):
    data = pd.read_csv(file_name, header=None)
    data.columns = ['�����', 'г�', '���������']
    data = data.sort_values(['�����', 'г�'])
    data['���� ���������'] = data.groupby('�����')['���������'].diff().fillna(0)
    return data

file_name = "population_data.txt"
population_data = test_population_change(file_name)
print(population_data)

