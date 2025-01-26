import re
from copy import deepcopy
from operator import methodcaller
from ..model.model import ContactList, Contact, ContactFile
from ..model.exceptions import (
    PhoneDataFileNotFoundError,
    RandomDataFileNotFoundError,
    NonUniqueId,
    NonIntId,
    CustomException,
    InvalidHeaders
)
from ..view.view import ContactListView
from ..constants import (
    HEADERS,
    CREATE_NEW_CONTACT_MENU,
    CHECK_PATTERNS_DICT,
    MENU_DICT
)


class MenuController():

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.contactlist = None
        self.old_contactlist = None

    def __check_data(data_item: str, headers_name: str) -> str:
        """ Проверяет строку данных на соответствие паттерну """
        pattern = CHECK_PATTERNS_DICT[headers_name]["pattern"]
        if not re.match(pattern, data_item.lower()):
            return CHECK_PATTERNS_DICT[headers_name]["hint"]

    def __check_input_data(str_for_input, default_input, headers_name) -> str:
        """ цикл проверки для ввода данных """
        hint = ""
        while hint is not None:
            data_item = input(str_for_input) or default_input
            hint = MenuController.__check_data(data_item, headers_name)
            if default_input == "=":
                hint = None
            if hint:
                data_item=None
                raise CustomException(f"{hint}. Повторите ввод данных.\n")
                #print(hint + " Повторите ввод данных.")
        return data_item

    def __create_input_data_list(input_names_list: list, default_input_list: list) -> list:
        """ Ввод новых данных """
        input_data = []
        for i in range(len(input_names_list)):
            str_for_input = f"{input_names_list[i]} {default_input_list[i]} => "
            data_item = MenuController.__check_input_data(
                str_for_input, default_input_list[i], HEADERS[i+1])
            input_data.append(data_item.strip())
        return input_data

    def find_data_from_id(self) -> tuple:
        data = None
        value_dict = None
        id = input("Введите id контакта => ")
        if id=="":
            value_dict = {"id": ""}
        if id.isnumeric():
            value_dict = {"id": int(id)}
            result = self.contactlist.find_id(value_dict)
            if result:
                data = self.contactlist.find(value_dict)
            return data, value_dict
        else:
            return None, value_dict

    def print_all_data_main(self):
        """ выполнение пункта Показать все контакты и вывод результата """
        all_data = self.contactlist.sort_contactlist()
        ContactListView.display_contact_list(all_data)
        return all_data

    def append_data_main(self):
        """ Выполнение пункта Создать контакт и вывод результата """
        print("Введите данные")
        default_input_list = [""]*len(CREATE_NEW_CONTACT_MENU)
        try:
            input_data = MenuController.__create_input_data_list(
                CREATE_NEW_CONTACT_MENU, default_input_list)
            print("\nДобавлены данные:")
            new_contact = Contact(*input_data)
            self.contactlist.append_contact(new_contact)
            found_data = self.contactlist.find(new_contact.data)
            # return found_data
            ContactListView.display_contact_list(found_data)
        except CustomException as e:
            print(e)

    def find_data_main(self)->'ContactList':
        """ Выполнение пункта Найти контакт и вывод результата """
        print("Введите данные для поиска или нажмите ввод для пропуска поля")
        data_from_id, value_dict = self.find_data_from_id()
        if value_dict!={"id":""} and data_from_id is None:
            print("Данные по id не найдены.\n")
        elif data_from_id and value_dict:
            ContactListView.display_contact_list(data_from_id)
            return data_from_id
        else:
            default_input_list = ["="]*len(CREATE_NEW_CONTACT_MENU)
            try:
                input_data = MenuController.__create_input_data_list(
                    CREATE_NEW_CONTACT_MENU, default_input_list)
                value_dict = dict([(x, y) for (x, y) in zip(
                HEADERS[1:], input_data) if y != "="])
                input_all_fields = input("Поиск по всем полям = =>")
                if input_all_fields:
                    value_dict.setdefault("*", input_all_fields)
                result = self.contactlist.find_id(value_dict)
                print(value_dict)
                if result:
                    found_data = self.contactlist.find(value_dict)
                    ContactListView.display_contact_list(found_data)
                    return found_data
                else:
                    print("Данные не найдены.\n")
            except CustomException as e:
                print(e)
            

    def remove_data_main(self):
        """ Выполнение пункта Удалить контакт и вывод результата """
        print("Для удаления:")
        data_to_delete, value_dict = self.find_data_from_id()
        if data_to_delete:
            print("\nУдалены данные:")
            # return data_to_delete
            ContactListView.display_contact_list(data_to_delete)
            self.contactlist.remove(value_dict)
        else:
            print("Данные для удаления не найдены.\n")

    def update_data_main(self):
        """ Выполнение пункта Изменить контакт (удалить + внести новые данные)  и вывод результата """
        print("Для изменения:")
        data_to_update, value_dict = self.find_data_from_id()
        if data_to_update:
            id = value_dict["id"]
            default_input_list = []
            for item in data_to_update.data[id]:
                print(item)
                default_input_list.append(item[1])
            print(default_input_list)
            try:
                input_data = MenuController.__create_input_data_list(
                    CREATE_NEW_CONTACT_MENU, default_input_list)
                self.contactlist.remove(value_dict)
                print("\nИзменены данные:")
                new_contact = Contact(*input_data)
                self.contactlist.append_contact(new_contact, id)
                found_data = self.contactlist.find(value_dict)
                # return found_data
                ContactListView.display_contact_list(found_data)
            except CustomException as e:
                print(e)
        else:
            print("Данные для изменения не найдены.\n")

    def save_data_main(self):
        """ Выполнение пункта Сохранить изменения и вывод результата """
        try:
            with ContactFile(self.filename, "write") as phonebook:
                phonebook.csv_export(self.contactlist)
                self.old_contactlist = deepcopy(self.contactlist)
                print("Данные сохранены.\n")
        except PhoneDataFileNotFoundError as e:
            print(f"DataFileNotFoundError {e}")

    def quit_phonebook_main(self) -> str:
        """ Выход из меню - получение значения для завершения работы """
        if self.contactlist != self.old_contactlist:
            input_data = ""
            while input_data not in ["y", "n", "Y", "N"]:
                input_data = input("Сохранить изменения? Y/N => ")
            if input_data in ["Y", "y"]:
                pass
                self.save_data_main()
        print("До новых встреч!")
        return "quit"

    def print_menu(self):
        """ Выбор в главном меню """
        quit_choice = None
        while quit_choice is None:
            choice = ContactListView.main_menu()
            if MENU_DICT.get(choice):
                method = methodcaller(MENU_DICT.get(choice)["def_name"])
                method(self)
                if MENU_DICT.get(choice)["def_name"] == "quit_phonebook_main":
                    quit_choice = 1
            else:
                print("Ошибка ввода.\n")

    def load_phonebook_data(self):
        try:
            with ContactFile(self.filename, "read") as phonebook:
                self.contactlist = phonebook.csv_import()
                self.old_contactlist = deepcopy(self.contactlist)
        except NonIntId as e:
            print(f"{self.filename} не соответствует требованиям: {e}")
        except NonUniqueId as e:
            print(f"{self.filename} не соответствует требованиям: {e}")
        except InvalidHeaders as e:
            print(f"{self.filename} не соответствует требованиям: {e}")
        except PhoneDataFileNotFoundError as e:
            #self.old_contactlist = ContactList()
            print(f'Телефонная книга {self.filename} не найдена. Создаем.\n')
            input_data = " "
            while input_data not in ["y", "n", "Y", "N"]:
                input_data = input("Сгенерировать рандомные данные? Y/N => ")
            if input_data in ["N", "n"]:
                self.contactlist=ContactList()
            if input_data in ["Y", "y"]:
                try:
                    self.contactlist = ContactList().generate_random(10)
                    print('Рандомные данные вставлены.\n')
                except RandomDataFileNotFoundError as e:
                    print(f"DataFileNotFoundError = > {e}")

    def enjoy_phonebook(self):
        """ Открытие существующей телефонной книги или создание новой, если ее нет """
        ContactListView.display_hello()
        self.load_phonebook_data()
        if self.contactlist:
            self.print_menu()


def main(filename: str):
    mc = MenuController(filename)
    mc.enjoy_phonebook()
