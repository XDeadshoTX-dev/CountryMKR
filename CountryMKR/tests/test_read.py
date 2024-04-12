# -*- coding: cp1251 -*-
import os
import pandas as pd
import pytest

# Фікстура для створення тестових даних
@pytest.fixture
def create_file():
    def _create_file(file_name, data):
        data.to_csv(file_name, header=False, index=False)
    return _create_file

# Параметризація для виконання тестів з різними наборами даних
@pytest.mark.parametrize('file_name, expected', [
    ('test_data1.txt', pd.DataFrame({
        'Країна': ['Україна', 'Україна'],
        'Рік': [2020, 2021],
        'Населення': [44134693, 43993638]
    })),
    ('test_data2.txt', pd.DataFrame({
        'Країна': ['Франція', 'Франція'],
        'Рік': [2020, 2021],
        'Населення': [145912025, 145912987]
    })),
])
def test_write(create_file, file_name, expected):
    create_file(file_name, expected)
    data = pd.read_csv(file_name, header=None)
    data.columns = ['Країна', 'Рік', 'Населення']
    pd.testing.assert_frame_equal(data, expected)

@pytest.mark.parametrize('file_name, expected', [
    ('test_data1.txt', pd.DataFrame({
        'Країна': ['Україна'],
        'Зміна населення': [float(43993638 - 44134693)]
    })),
    ('test_data2.txt', pd.DataFrame({
        'Країна': ['Франція'],
        'Зміна населення': [float(145912987 - 145912025)]
    })),
])
def test_population_change(file_name, expected):
    data = pd.read_csv(file_name, header=None)
    data.columns = ['Країна', 'Рік', 'Населення']
    data = data.sort_values(['Країна', 'Рік'])
    data['Зміна населення'] = data.groupby('Країна')['Населення'].diff().fillna(0)
    data = data.groupby('Країна')['Зміна населення'].sum().reset_index()
    pd.testing.assert_frame_equal(data, expected)
    # Видалення файлу після виконання тесту
    os.remove(file_name)