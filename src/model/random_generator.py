import random
import json
from .exceptions import RandomDataFileNotFoundError
from ..constants import (
    NAMES_FILE,
    PHONECODES_FILE,
)

# Заменена на random.choice
# def random_data(data: list) -> list:
#     """ Выбирает рандомное значение в списке """
#     return data[random.randint(0, len(data)-1)]


def random_name() -> tuple:
    """ Генерирует рандомное имя-фамилия из файла random_names.json """
    try:
        with open(NAMES_FILE, 'r', encoding='UTF-8') as file:
            file_data = json.load(file)
        sex = random.choice(["male", "female"])
        surnames = file_data[sex]["surname"]
        names = file_data[sex]["name"]
        return random.choice(surnames), random.choice(names)
    except FileNotFoundError:
        raise RandomDataFileNotFoundError(NAMES_FILE)


def random_phone() -> tuple:
    """ Генерирует рандомный телефон из "+"" и 12 цифр: код страны + остальные рандомные """
    try:
        with open(PHONECODES_FILE, 'r', encoding='UTF-8') as file:
            file_data = [x.strip().split('\t') for x in file.readlines()]
            phonecodes = {}
        for x in file_data:
            phonecodes.setdefault(x[1], x[0])
        country_code = random.choice(file_data)[1]
        phone_number = country_code+" " + \
            str(random.choice(range(10**(12-len(country_code)+1))))
        country = phonecodes.get(phone_number.split()[0])
        return phone_number, country
    except FileNotFoundError:
        raise RandomDataFileNotFoundError(PHONECODES_FILE)


if __name__ == '__main__':
    random_name()
    random_phone()