import os
import random
import string

import pandas as pd


def random_passwords(file_name: str, word_length: int, prefix='Password'):
    """
    为每个学生生成密码, 输出文件在源文件名称前添加password

    Parameters
    ----------
    file_name: 源文件, panda可读, 第一列为名称
    word_length: 密码长度
    prefix: 用于生成文件的前缀, 同时也作为密码列
    """
    if not os.path.exists(file_name):
        return print(f'file: {file_name} not exists')
    students = pd.read_excel(file_name)
    # 利用字典, 保证相同名字相同输出
    dic = {}
    for row in students.itertuples():
        # dic中不存在, 去一个随机密码
        if not row[1] in dic:
            dic[row[1]] = random_password(word_length)
        # 赋予密码
        students.at[row[0], prefix] = dic[row[1]]
    # 保存文件(与源文件区别)
    students.to_excel(f'{prefix}.{file_name}', index=False)
    print(f'save file to {prefix}.{file_name}')


def random_password(word_length: int) -> str:
    password = [random.choice(string.ascii_letters) for _ in range(word_length - 2)]
    password.append(random.choice(string.digits))
    password.append(random.choice(string.punctuation))
    random.shuffle(password)
    return ''.join(password)


def _single_password():
    print('start')
    while True:
        length = input('input length of password:')
        if length == 'exit':
            break
        if not length.isdigit():
            print('error input, should be a digit')
            continue
        length = int(length)
        if length > 32 or length < 6:
            print('error input, length should be more then 6 and less then 32')
            continue
        print(random_password(length))

    print('exit')


if __name__ == '__main__':
    random_passwords('students.xlsx', 12)
