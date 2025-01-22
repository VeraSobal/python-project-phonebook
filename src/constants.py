import os
# csv-файл с данными для телефонной книги
PHONE_BOOK = './data/phonebook.csv'
# файл для генерации случайных имен
NAMES_FILE = './data/names.json'
# файл для генерации случайных телефонных номеров
PHONECODES_FILE = './data/phonecodes.txt'
# заголовки данных телефонной книги
HEADERS = ["id", "surname", "name", "phone", "comment"]
# заголовки меню для создания нового контакта
CREATE_NEW_CONTACT_MENU = ["Фамилия", "Имя", "Номер телефона", "Комментарий"]
# заголовки главного меню и имена функций для выполнения пунктов меню
MENU_DICT = {
    "1": {"menu_item": "Показать все контакты", "def_name": "print_all_data_main"},
    "2": {"menu_item": "Создать контакт", "def_name": "append_data_main"},
    "3": {"menu_item": "Найти контакт", "def_name": "find_data_main"},
    "4": {"menu_item": "Изменить контакт", "def_name": "update_data_main"},
    "5": {"menu_item": "Удалить контакт", "def_name": "remove_data_main"},
    "6": {"menu_item": "Сохранить изменения", "def_name": "save_data_main"},
    "7": {"menu_item": "Завершить работу", "def_name": "quit_phonebook_main"},
}
# заголовки меню для поиска контактов
FIND_CONTACT_MENU = ["По всем колонкам", "Номер",
                     "Фамилия", "Имя", "Номер телефона", "Комментарий"]

# буквы, потом опционально тире с буквами
word_pattern = r'[a-zа-яё]+(?:-[a-zа-яё]+)*'
name_pattern = r"{}".format(f'^{word_pattern}[ ]*({word_pattern})*$')
phone_pattern = r'^[+]*[0-9]+(?:[0-9 ]+)*$'
comment_pattern = r''

# ключи словаря должны совпадать с полями класса Contact
CHECK_PATTERNS_DICT = {
    "surname": {"pattern": name_pattern, "hint": "Допустимы буквы, пробел и - внутри."},
    "name": {"pattern": name_pattern, "hint": "Допустимы буквы, пробел и - внутри."},
    "phone": {"pattern": r'^[+]*[0-9]+(?:[0-9 ]+)*$', "hint": "+(опционально), затем цифры, пробелы."},
    "comment": {"pattern": r'', "hint": ""}
}
