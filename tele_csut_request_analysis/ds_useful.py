import pandas as pd


def conv_dt(data_dt,to):
    result = []
    if to == 'int':
        for i in data_dt:
            result.append(int(i))
    if to == 'str':
        for i in data_dt:
            result.append(str(i))
    return result