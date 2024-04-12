# -*- coding: cp1251 -*-
import os
import pandas as pd
import pytest

# Գ������ ��� ��������� �������� �����
@pytest.fixture
def create_file():
    def _create_file(file_name, data):
        data.to_csv(file_name, header=False, index=False)
    return _create_file

# �������������� ��� ��������� ����� � ������ �������� �����
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
def test_write(create_file, file_name, expected):
    create_file(file_name, expected)
    data = pd.read_csv(file_name, header=None)
    data.columns = ['�����', 'г�', '���������']
    pd.testing.assert_frame_equal(data, expected)

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
    pd.testing.assert_frame_equal(data, expected)
    # ��������� ����� ���� ��������� �����
    os.remove(file_name)