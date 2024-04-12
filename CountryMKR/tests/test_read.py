# -*- coding: cp1251 -*-
import os
import pandas as pd
import pytest

# Fixture for creating test data
@pytest.fixture
def create_file():
    def _create_file(file_name, data):
        data.to_csv(file_name, header=False, index=False)
    return _create_file

# Parametrization for running tests with different sets of data
@pytest.mark.parametrize('file_name, expected', [
    ('test_data1.txt', pd.DataFrame({
        'Country': ['Ukraine', 'Ukraine'],
        'Year': [2020, 2021],
        'Population': [44134693, 43993638]
    })),
    ('test_data2.txt', pd.DataFrame({
        'Country': ['France', 'France'],
        'Year': [2020, 2021],
        'Population': [145912025, 145912987]
    })),
])
def test_write(create_file, file_name, expected):
    create_file(file_name, expected)
    data = pd.read_csv(file_name, header=None)
    data.columns = ['Country', 'Year', 'Population']
    pd.testing.assert_frame_equal(data, expected)

@pytest.mark.parametrize('file_name, expected', [
    ('test_data1.txt', pd.DataFrame({
        'Country': ['Ukraine'],
        'Population Change': [float(43993638 - 44134693)]
    })),
    ('test_data2.txt', pd.DataFrame({
        'Country': ['France'],
        'Population Change': [float(145912987 - 145912025)]
    })),
])
def test_population_change(file_name, expected):
    data = pd.read_csv(file_name, header=None)
    data.columns = ['Country', 'Year', 'Population']
    data = data.sort_values(['Country', 'Year'])
    data['Population Change'] = data.groupby('Country')['Population'].diff().fillna(0)
    data = data.groupby('Country')['Population Change'].sum().reset_index()
    pd.testing.assert_frame_equal(data, expected)
    # Deleting the file after the test is run
    os.remove(file_name)
