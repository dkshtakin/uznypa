import os
import pickle


def load_list(filename):
    data_list = []
    if not os.path.isfile(filename):
        return data_list
    with open(filename, "rb") as file:
        while True:
            try:
                data_list += pickle.load(file)
            except EOFError:
                return data_list


def save_list(filename, data_list, overwrite=False):
    mode = 'wb' if overwrite else 'ab'
    with open(filename, mode) as file:
        pickle.dump(data_list, file)


def load_value(filename):
    if not os.path.isfile(filename):
        return 0
    with open(filename, "rb") as file:
        return pickle.load(file)


def save_value(filename, value):
    with open(filename, "wb") as file:
        pickle.dump(value, file)
