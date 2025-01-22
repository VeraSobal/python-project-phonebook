from ..model.model import Contact, ContactList
from ..constants import(
    MENU_DICT
)


class ContactListView:

    @staticmethod
    def display_contact(contact: Contact):
        """Отображает контакт"""
        print(contact)
        print()

    @staticmethod
    def display_contact_list(contactlist: ContactList):
        """Отображает список контактов"""
        print("Результат:")
        print(contactlist)
        print()

    @staticmethod
    def display_hello():
        """Отображает приветствие"""
        print("***Приветствую!***")

    @staticmethod
    def main_menu()->str:
        """Отображает главное меню"""
        print("Меню телефонной книги: ")
        for key, value in MENU_DICT.items():
            print(f'{key}. {value["menu_item"]}')
        print()
        choice = input("Выберите пункт меню => ")
        return choice

