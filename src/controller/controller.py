import sys
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
from ..view.view import PhonebookView
from ..constants import (
    PHONE_BOOK,
    HEADERS,
    CREATE_NEW_CONTACT_MENU,
    MENU_DICT,
    INPUT_MESSAGE,
    OUTPUT_MESSAGE
)


class MenuController():

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.contactlist = None
        self.old_contactlist = None

    def find_data_from_id(self) -> tuple:
        data = None
        value_dict = None
        id = PhonebookView.input_message(INPUT_MESSAGE["id"])
        if id == "":
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
        PhonebookView.display_contact_list(all_data)
        return all_data

    def append_data_main(self):
        """ Выполнение пункта Создать контакт и вывод результата """
        PhonebookView.display_message(OUTPUT_MESSAGE["input"])
        default_input_list = [""]*len(CREATE_NEW_CONTACT_MENU)
        try:
            input_data = PhonebookView.create_input_data_list(
                CREATE_NEW_CONTACT_MENU, default_input_list)
            PhonebookView.display_message(OUTPUT_MESSAGE["appended"])
            new_contact = Contact(*input_data)
            self.contactlist.append_contact(new_contact)
            found_data = self.contactlist.find(new_contact.data)
            PhonebookView.display_contact_list(found_data)
        except CustomException as e:
            PhonebookView.display_error(e)

    def find_data_main(self) -> 'ContactList':
        """ Выполнение пункта Найти контакт и вывод результата """
        PhonebookView.display_message(OUTPUT_MESSAGE["for_find"])
        data_from_id, value_dict = self.find_data_from_id()
        if value_dict != {"id": ""} and data_from_id is None:
            PhonebookView.display_message(OUTPUT_MESSAGE["not_found"])
        elif data_from_id and value_dict:
            PhonebookView.display_contact_list(data_from_id)
            return data_from_id
        else:
            default_input_list = ["="]*len(CREATE_NEW_CONTACT_MENU)
            try:
                input_data = PhonebookView.create_input_data_list(
                    CREATE_NEW_CONTACT_MENU, default_input_list)
                value_dict = dict([(x, y) for (x, y) in zip(
                    HEADERS[1:], input_data) if y != "="])
                input_all_fields = PhonebookView.input_message(
                    INPUT_MESSAGE["all_fields"])
                if input_all_fields:
                    value_dict.setdefault("*", input_all_fields)
                result = self.contactlist.find_id(value_dict)
                if result:
                    found_data = self.contactlist.find(value_dict)
                    PhonebookView.display_contact_list(found_data)
                    return found_data
                else:
                    PhonebookView.display_message(OUTPUT_MESSAGE["not_found"])
            except CustomException as e:
                PhonebookView.display_error(e)

    def remove_data_main(self):
        """ Выполнение пункта Удалить контакт и вывод результата """
        PhonebookView.display_message(OUTPUT_MESSAGE["for_remove"])
        data_to_delete, value_dict = self.find_data_from_id()
        if data_to_delete:
            PhonebookView.display_message(OUTPUT_MESSAGE["removed"])
            PhonebookView.display_contact_list(data_to_delete)
            self.contactlist.remove(value_dict)
        else:
            PhonebookView.display_message(OUTPUT_MESSAGE["not_found"])

    def update_data_main(self):
        """ Выполнение пункта Изменить контакт (удалить + внести новые данные)  и вывод результата """
        PhonebookView.display_message(OUTPUT_MESSAGE["for_update"])
        data_to_update, value_dict = self.find_data_from_id()
        if data_to_update:
            id = value_dict["id"]
            default_input_list = []
            for item in data_to_update.data[id]:
                default_input_list.append(item[1])
            try:
                input_data = PhonebookView.create_input_data_list(
                    CREATE_NEW_CONTACT_MENU, default_input_list)
                self.contactlist.remove(value_dict)
                PhonebookView.display_message(OUTPUT_MESSAGE["updated"])
                new_contact = Contact(*input_data)
                self.contactlist.append_contact(new_contact, id)
                found_data = self.contactlist.find(value_dict)
                PhonebookView.display_contact_list(found_data)
            except CustomException as e:
                PhonebookView.display_error(e)
        else:
            PhonebookView.display_message(OUTPUT_MESSAGE["not_found"])

    def save_data_main(self):
        """ Выполнение пункта Сохранить изменения и вывод результата """
        try:
            with ContactFile(self.filename, "write") as phonebook:
                phonebook.csv_export(self.contactlist)
                self.old_contactlist = deepcopy(self.contactlist)
                PhonebookView.display_message(OUTPUT_MESSAGE["saved"])
        except PhoneDataFileNotFoundError as e:
            PhonebookView.display_error(f"DataFileNotFoundError {e}")

    def quit_phonebook_main(self) -> str:
        """ Выход из меню - получение значения для завершения работы """
        if self.contactlist != self.old_contactlist:
            input_data = PhonebookView.input_yn_message(
                INPUT_MESSAGE["yn_save"])
            if input_data in ["Y", "y"]:
                self.save_data_main()
        PhonebookView.display_bye()
        return "quit"

    def print_menu(self):
        """ Выбор в главном меню """
        quit_choice = None
        while quit_choice is None:
            choice = PhonebookView.main_menu()
            if MENU_DICT.get(choice):
                method = methodcaller(MENU_DICT.get(choice)["def_name"])
                method(self)
                if MENU_DICT.get(choice)["def_name"] == "quit_phonebook_main":
                    quit_choice = 1
            else:
                PhonebookView.display_message(OUTPUT_MESSAGE["error_input"])

    def load_phonebook_data(self):
        """Загрузка данных из файла"""
        try:
            with ContactFile(self.filename, "read") as phonebook:
                self.contactlist = phonebook.csv_import()
                self.old_contactlist = deepcopy(self.contactlist)
        except NonIntId as e:
            PhonebookView.display_error(
                f"{self.filename} не соответствует требованиям: {e}")
        except NonUniqueId as e:
            PhonebookView.display_error(
                f"{self.filename} не соответствует требованиям: {e}")
        except InvalidHeaders as e:
            PhonebookView.display_error(
                f"{self.filename} не соответствует требованиям: {e}")
        except PhoneDataFileNotFoundError as e:
            PhonebookView.display_error(
                f'Телефонная книга {self.filename} не найдена. Создаем.\n')
            input_data = PhonebookView.input_yn_message(
                INPUT_MESSAGE["yn_random"])
            if input_data in ["N", "n"]:
                self.contactlist = ContactList()
            if input_data in ["Y", "y"]:
                try:
                    self.contactlist = ContactList().generate_random(10)
                    PhonebookView.display_message(
                        OUTPUT_MESSAGE["random_input"])
                except RandomDataFileNotFoundError as e:
                    PhonebookView.display_error(
                        f"DataFileNotFoundError = > {e}")


def enjoy_phonebook(filename=PHONE_BOOK):
    """ Открытие существующей телефонной книги или создание новой, если ее нет """
    mc = MenuController(filename)
    PhonebookView.display_hello()
    mc.load_phonebook_data()
    if mc.contactlist:
        mc.print_menu()

def main(filename=PHONE_BOOK):
    enjoy_phonebook()
