import random
import string


def random_password(word_length: int) -> str:
    password = [random.choice(string.ascii_letters) for _ in range(word_length - 2)]
    password.append(random.choice(string.digits))
    password.append(random.choice(string.punctuation))
    random.shuffle(password)
    return ''.join(password)


if __name__ == '__main__':
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
