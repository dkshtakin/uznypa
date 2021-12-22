"""Serialization/deserialization test for pytest"""
import os
from saving import load_list, save_list, load_value, save_value


def test_serialization():
    """Serialization/deserialization test"""
    dct = {'field1': 'some_string', 'field2': '18926938264'}
    filename = 'somevalue.txt'
    save_value(filename, dct)
    dct_load = load_value(filename)
    assert dct == dct_load
    os.remove(filename)

    filename = 'somelist.txt'
    lst = ['hello', 'how', 'are', 'you', 'doing', 'today']
    save_list(filename, lst)
    lst_load = load_list(filename)
    assert lst == lst_load
    save_list(filename, ['new_string'])
    lst.append('new_string')
    lst_load = load_list(filename)
    assert lst == lst_load
    lst = ['absolutely', 'new', 'list']
    save_list(filename, lst, True)
    lst_load = load_list(filename)
    assert lst == lst_load
    os.remove(filename)
