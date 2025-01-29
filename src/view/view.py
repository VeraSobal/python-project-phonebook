import re
#from ..model.model import Contact, ContactList
from ..constants import(
    MENU_DICT,
    CHECK_PATTERNS_DICT,
    HEADERS
)
from ..model.exceptions import CustomException


class PhonebookView:

    def __init__(self):
        pass

    @staticmethod
    def display_contact(contact: 'Contact'):
        """Отображает контакт"""
        print(contact)
        print()

    @staticmethod
    def display_contact_list(contactlist: 'ContactList'):
        """Отображает список контактов"""
        print("Результат:")
        print(contactlist)
        print()

    @staticmethod
    def display_hello():
        """Отображает приветствие"""
        print("***Приветствую!***")

    @staticmethod
    def display_bye():
        """Отображает окончание работы"""
        print("***До новых встреч!***")

    @staticmethod
    def display_message(message):
        """Отображает информационную строку"""
        print(message)

    @staticmethod
    def display_error(message):
        """Отображает информационную строку"""
        print(message)

    @staticmethod
    def main_menu()->str:
        """Отображает главное меню"""
        print("Меню телефонной книги: ")
        for key, value in MENU_DICT.items():
            print(f'{key}. {value["menu_item"]}')
        print()
        choice = input("Выберите пункт меню => ")
        return choice
    
    @staticmethod
    def input_message(message:str)->chr:
        """Принимает ответ пользователя"""
        return input(message)
    
    @staticmethod
    def input_yn_message(message:str)->chr:
        """Принимает ответ пользователя в рамках y-n"""
        input_data = ""
        while input_data not in ["y", "n", "Y", "N"]:
            input_data = input(message)
        return input_data
    
    @staticmethod
    def check_data(data_item: str, headers_name: str) -> str:
        """ Проверяет строку данных на соответствие паттерну """
        pattern = CHECK_PATTERNS_DICT[headers_name]["pattern"]
        if not re.match(pattern, data_item.lower()):
            return CHECK_PATTERNS_DICT[headers_name]["hint"]

    @staticmethod
    def check_input_data(str_for_input, default_input, headers_name) -> str:
        """ цикл проверки для ввода данных """
        hint = ""
        while hint is not None:
            data_item = input(str_for_input) or default_input
            hint = PhonebookView.check_data(data_item, headers_name)
            if default_input == "=":
                hint = None
            if hint:
                data_item=None
                raise CustomException(f"{hint}. Повторите ввод данных.\n")
                #print(hint + " Повторите ввод данных.")
        return data_item

    @staticmethod
    def create_input_data_list(input_names_list: list, default_input_list: list) -> list:
        """ Ввод новых данных """
        input_data = []
        for i in range(len(input_names_list)):
            str_for_input = f"{input_names_list[i]} {default_input_list[i]} => "
            data_item = PhonebookView.check_input_data(
                str_for_input, default_input_list[i], HEADERS[i+1])
            input_data.append(data_item.strip())
        return input_data
