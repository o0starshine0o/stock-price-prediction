import os
import time

from makesentence import sentence


def spend(func):
    def calc_time(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f'{func.__name__} spend: {time.time() - start} second, with result: {result}')
        return result

    return calc_time


def _create_data(count: int):
    data = []
    for _ in range(count):
        data.append(sentence())
    return data


def _write_data(path: str, name: str, data: list):
    if not _file_exist(path):
        os.makedirs(path)
    with open(path + name, 'w') as file:
        file.writelines([' '.join(text) + '\n' for text in data])


@spend
def _read_encoding(filename):
    with open(filename, encoding="utf_8") as f:
        return sum(sum(1 for word in line.split() if word == 'cat') for line in f)


@spend
def _read_file(filename):
    with open(filename, 'r') as f:
        return sum(1 for word in f.read().split() if word == 'cat')


@spend
def _read_line(filename):
    with open(filename, 'r') as f:
        return sum(sum(1 for word in line.split() if word == 'cat') for line in f.readlines())


def _file_exist(path: str) -> bool:
    return path and os.path.exists(path)


if __name__ == "__main__":
    _write_data('logs/', 'sentence.txt', _create_data(100000000))
    _read_encoding('logs/sentence.txt')
    _read_file('logs/sentence.txt')
    _read_line('logs/sentence.txt')
    exit()
