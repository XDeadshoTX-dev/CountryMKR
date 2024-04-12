# -*- coding: cp1251 -*-
import os
import pandas as pd
import pytest

@pytest.mark.parametrize('file_name, expected', [
    ('test_data1.txt', pd.DataFrame({
        '�����': ['������', '������'],
        'г�': [2020, 2021],
        '���������': [44134693, 43993638]
    })),
    ('test_data2.txt', pd.DataFrame({
        '�����': ['�������', '�������'],
        'г�': [2020, 2021],
        '���������': [145912025, 145912987]
    })),
])
def test_write(file_name, expected):
    expected.to_csv(file_name, header=False, index=False)

@pytest.mark.parametrize('file_name, expected', [
    ('test_data1.txt', pd.DataFrame({
        '�����': ['������'],
        '���� ���������': [float(43993638 - 44134693)]
    })),
    ('test_data2.txt', pd.DataFrame({
        '�����': ['�������'],
        '���� ���������': [float(145912987 - 145912025)]
    })),
])

def test_population_change(file_name, expected):
    data = pd.read_csv(file_name, header=None)
    data.columns = ['�����', 'г�', '���������']
    data = data.sort_values(['�����', 'г�'])
    data['���� ���������'] = data.groupby('�����')['���������'].diff().fillna(0)
    data = data.groupby('�����')['���� ���������'].sum().reset_index()
    print(data)
    pd.testing.assert_frame_equal(data, expected)

