#!/usr/bin/env python3

import json
import csv
import random
import re
import ast
from copy import deepcopy
from constants import (
    PHONE_BOOK,
    NAMES_FILE,
    PHONECODES_FILE,
    HEADERS,
    FIND_CONTACT_MENU,
    CREATE_NEW_CONTACT_MENU,
    MENU_DICT,
    CHECK_PATTERNS_DICT,
)


def random_data(data: list) -> list:
    """ Выбирает рандомное значение в списке """
    return data[random.randint(0, len(data)-1)]


def random_name() -> tuple:
    """ Генерирует рандомное имя-фамилия из файла random_names.json """
    with open(NAMES_FILE, 'r', encoding='UTF-8') as file:
        file_data = json.load(file)
    sex = random_data(["male", "female"])
    surnames = file_data[sex]["surname"]
    names = file_data[sex]["name"]
    return random_data(surnames), random_data(names)


def random_phone() -> tuple:
    """ Генерирует рандомный телефон из "+"" и 12 цифр: код страны + остальные рандомные """
    with open(PHONECODES_FILE, 'r', encoding='UTF-8') as file:
        file_data = [x.strip().split('\t') for x in file.readlines()]
        phonecodes = {}
    for x in file_data:
        phonecodes.setdefault(x[1], x[0])
    country_code = random_data(file_data)[1]
    phone_number = country_code+" " + \
        str(random_data(range(10**(12-len(country_code)+1))))
    country = phonecodes.get(phone_number.split()[0])
    return phone_number, country


def max_len(data: list, i: int) -> int:
    """ Вычисление максимальной длины строк в каждом столбце  для красивого вывода на экран """
    return max([len(x[i]) for x in data])


def align_data(data: list, col_length: list) -> list:
    """ Форматирование строки (col_length - список с шириной для каждого столбца) """
    f_align_data = []
    for item in data:
        formatted_item = [
            f"{item[i]:<{col_length[i]+1}}" for i in range(len(item))]
        f_align_data.append("|".join(formatted_item))
    return f_align_data


def print_lines(lines_qty):
    """ Декоратор - добавление пустых строк в вывод """
    def decorator(func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
            print("\n"*lines_qty)
        return wrapper
    return decorator


@print_lines(1)
def print_data(data: list, lines_per_page=20, start_col=0):
    """ Вывод данных на экран в виде таблицы; если start_col=1, то берет данные без id """
    col_length = []
    for i in range(len(HEADERS)):
        col_length.append(max_len((data if data != [] else [HEADERS]), i))
    col_length = col_length[start_col:]
    for i in range(len(col_length)):
        if len(HEADERS[i]) > col_length[i]:
            col_length[i] = len(HEADERS[i])
    data_to_print = align_data([x[start_col:] for x in data], col_length)
    headers_to_print = align_data([HEADERS[start_col:]], col_length)
    pages_qty = (len(data_to_print))//lines_per_page + \
        (0 if (len(data_to_print)) % lines_per_page == 0 else 1)
    pages_qty = max(pages_qty, 1)
    i = 1
    quit_key = ""
    while i <= pages_qty and quit_key != "q":
        print(*headers_to_print)
        print('-'*(sum(col_length)+2*len(col_length)))
        print(*data_to_print[(i-1)*lines_per_page:min(i *
              lines_per_page, len(data_to_print))], sep="\n")
        if pages_qty > 1:
            print(f"- страница {i} -", "\n")
        if i != pages_qty:
            quit_key = input(
                "Enter - следующая страница или q - завершить просмотр ")
            print("\n")
        i += 1


def check_data(data_item: str, headers_name: str) -> str:
    """ Проверяет строку данных на соответствие паттерну """
    pattern = CHECK_PATTERNS_DICT[headers_name]["pattern"]
    if not re.match(pattern, data_item.lower()):
        return CHECK_PATTERNS_DICT[headers_name]["hint"]


def find_data(data: list, data_to_find, col_index=-1) -> list:
    """ Поиск данных """
    find_index = []
    if col_index in list(range(len(HEADERS))):
        for i in range(len(data)):
            if str(data[i][col_index]).lower() == str(data_to_find).lower():
                find_index.append(data[i][0])  # сохраняем id
        return find_index
    elif col_index == -1:
        for i in range(len(HEADERS)):
            find_index += find_data(data, data_to_find, i)
        return find_index
    else:
        print("Неверная колонка!")


def filter_data(data: list, id: list) -> list:
    """ Получение данных по заданным id """
    filtered_data = list(filter(lambda x: x[0] in id, data))
    return filtered_data


def append_data(data: list, data_to_append: list, id) -> list:
    """ Запись новых данных """
    data_to_append = [str(id)]+data_to_append
    data.append(data_to_append)
    return [data_to_append]


def append_random_data(data: list, qty) -> list:
    """ Запись новых рандомных данных """
    result = []
    for _ in range(qty):
        new_id = (1 if len(data) == 0 else max([int(x[0]) for x in data])+1)
        random_data = [str(new_id), *random_name(), *random_phone()]
        result.append(random_data)
        append_data(data, random_data, new_id)
    return result


def delete_data(data: list, data_to_delete: list):
    """ Удаление данных """
    for x in data_to_delete:
        data.remove(x)


def update_data(data: list, data_to_update: list):
    """ Изменение данных """
    for x in data_to_update:
        data.remove(x)
        data.append(x)


def print_all_data_main(data: list):
    """ выполнение пункта Показать все контакты и вывод результата """
    print_data(sorted(data, key=lambda x: int(x[0])))


def check_input_data(str_for_input, default_input, headers_name) -> str:
    """ цикл проверки для ввода данных """
    hint = ""
    while hint is not None:
        data_item = input(str_for_input) or default_input
        hint = check_data(data_item, headers_name)
        if hint:
            print(hint + " Повторите ввод данных.")
    return data_item


def create_input_data_list(input_names_list: list, default_input_list: list) -> list:
    """ Ввод новых данных """
    input_data = []
    for i in range(len(input_names_list)):
        str_for_input = f"{input_names_list[i]} {default_input_list[i]} => "
        data_item = check_input_data(
            str_for_input, default_input_list[i], HEADERS[i+1])
        input_data.append(data_item.strip())
    return input_data


def append_data_main(data: list):
    """ Выполнение пункта Создать контакт и вывод результата """
    print("Введите данные")
    default_input_list = [""]*len(CREATE_NEW_CONTACT_MENU)
    input_data = create_input_data_list(
        CREATE_NEW_CONTACT_MENU, default_input_list)
    print("\nДобавлены данные:")
    new_id = (1 if len(data) == 0 else max([int(x[0]) for x in data])+1)
    print_data(append_data(data, input_data, new_id))


def find_data_main(data: list):
    """ Выполнение пункта Найти контакт и вывод результата """
    for i in range(len(FIND_CONTACT_MENU)):
        print(i, FIND_CONTACT_MENU[i])
    input_data_col = int(input("Выберите вариант поиска => "))-1
    input_data = input("Введите данные для поиска => ")
    result = find_data(data, input_data, input_data_col)
    if result != []:
        print_data(filter_data(data, result))
    else:
        print("Данные не найдены.\n")


def delete_data_main(data: list):
    """ Выполнение пункта Удалить контакт и вывод результата """
    id_for_delete = input("Введите id контакта для удаления => ")
    result = find_data(data, id_for_delete)
    if result != []:
        data_to_delete = filter_data(data, result)
        print("\nУдалены данные:")
        print_data(data_to_delete)
        delete_data(data, data_to_delete)
    else:
        print("Данные для удаления не найдены.\n")


def update_data_main(data: list):
    """ Выполнение пункта Изменить контакт (удалить + внести новые данные)  и вывод результата """
    id_for_update = input("Введите id контакта для изменения => ")
    result = find_data(data, id_for_update)
    if result != []:
        data_to_update = filter_data(data, result)
        print_data(data_to_update)
        default_input_list = data_to_update[0][1:]  # [1:] - чтобы без id
        input_data = create_input_data_list(
            CREATE_NEW_CONTACT_MENU, default_input_list)
        delete_data(data, data_to_update)
        print("\nИзменены данные:")
        print_data(append_data(data, input_data, result[0]))
    else:
        print("Данные для изменения не найдены.\n")


def write_to_file(data: list, file):
    """ Сохранение данных в файл """
    file.write(",".join(str(x) for x in HEADERS)+"\n")
    for item in data:
        file.write(",".join(str(x) for x in item)+"\n")


def save_data_main(data: list, old_data:list)->list:
    """ Выполнение пункта Сохранить изменения и вывод результата """
    try:
        with open(PHONE_BOOK, 'w', encoding='UTF-8') as file:
            write_to_file(data, file)
            old_data = deepcopy(data)
            print("Данные сохранены.\n")
    except:
        print("Ошибка!\n")
    return old_data


def quit_phonebook_main(data: list, old_data: list) -> str:
    """ Выход из меню - получение значения для завершения работы """
    if data != old_data:
        input_data = ""
        while input_data not in ["y", "n", "Y", "N"]:
            input_data = input("Сохранить изменения? Y/N => ")
        if input_data in ["Y", "y"]:
            old_data=save_data_main(data, old_data)
    print("До новых встреч!")
    return "quit"


def print_menu(data: list):
    """ Выбор в главном меню """
    old_data = deepcopy(data)
    quit_choice = None
    while quit_choice is None:
        print("Меню телефонной книги: ")
        for key, value in MENU_DICT.items():
            print(f'{key}. {value["menu_item"]}')
        choice = input("Выберите пункт меню => ")
        print()
        if MENU_DICT.get(choice):
            def_name = MENU_DICT.get(choice)["def_name"]
            if def_name == "print_all_data_main":
                print_all_data_main(data)
            elif def_name == "append_data_main":
                append_data_main(data)
            elif def_name == "find_data_main":
                find_data_main(data)
            elif def_name == "update_data_main":
                update_data_main(data)
            elif def_name == "delete_data_main":
                delete_data_main(data)
            elif def_name == "save_data_main":
                old_data = save_data_main(data, old_data)
            elif def_name == "quit_phonebook_main":
                quit_choice=quit_phonebook_main(data, old_data)
        else:
            print("Ошибка ввода.\n")


def enjoy_phonebook():
    """ Открытие существующей телефонной книги или создание новой, если ее нет """
    try:
        with open(PHONE_BOOK, 'r', encoding='UTF-8') as file:
            file_reader = csv.reader(file, delimiter=",", lineterminator="\n")
            data = [x for x in file_reader][1:]
    except:
        print('Телефонная книга не найдена. Создаем.\n')
        with open(PHONE_BOOK, 'x', encoding='UTF-8') as file:
            input_data = " "
            while input_data not in ["y", "n", "Y", "N"]:
                input_data = input("Вставить рандомные данные? Y/N => ")
            if input_data not in ["Y", "y"]:
                data = []
            else:
                data = append_random_data([], 20)
                print('Рандомные данные вставлены.\n')
            write_to_file(data, file)
    print_menu(data)


if __name__ == '__main__':
    enjoy_phonebook()
