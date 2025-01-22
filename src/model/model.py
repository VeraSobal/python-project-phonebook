import csv
from .random_generator import random_name, random_phone
from .exceptions import (
    CustomException,
    PhoneDataFileNotFoundError,
    FieldNotFound,
    NotDictionaryFormat,
    NonUniqueId
)
from ..constants import (
    CHECK_PATTERNS_DICT,
    HEADERS
)


class Contact:

    def __init__(self, surname: str, name: str, phone: str, comment: str):
        self.data = {"surname": surname, "name": name,
                     "phone": phone, "comment": comment}
        self.start = -1

    def __eq__(self, other):
        return (self.data == other.data)

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        if self.start < len(self.data.items()):
            return list(self.data.items())[self.start]
        raise StopIteration

    @classmethod
    def generate_random(cls) -> 'Contact':
        """Генерирует рандомный контакт"""
        return cls(*random_name(), *random_phone())

    def apply_new_data(self, new_data: dict):
        """Проводит проверки передаваемых в контакт значений. 
        Если значения не удовлетворяют условию, то контакт не меняется
        Числовые значения переводятся в строки """
        if isinstance(new_data, dict):
            for key, value in new_data.items():
                if key in self.data:
                    self.data[key] = str(value).strip()
                else:
                    raise FieldNotFound

    @property
    def len_data(self) -> dict:
        """Вычисляет длину поля для печати"""
        len_data_dict = {}
        for key, value in self.data.items():
            len_data_dict.setdefault(key, max(len(value), len(key)))
        return len_data_dict

    def __str__(self) -> str:
        """Приводит данные контакта в вид для печати"""
        headers = []
        print_item = []
        for key in CHECK_PATTERNS_DICT.keys():
            headers.append(f"{key:<{self.len_data[key]}}")
        for key, value in self.data.items():
            print_item.append(f"{value:<{self.len_data[key]}}")
        print_str = "| ".join(headers)+"\n"+"| ".join(print_item)+"\n"
        return print_str

    def __repr__(self) -> dict:
        return str(self.data)

    def isfound(self,  value_dict: dict) -> bool:
        """Проверяет соответствие значения поля значению этого поля контакте.
        если передается словарь c условием  "имя поля":"значение", то значение ищется только в этом поле контакта
        если в словаре несколько значений-условий, то считается удовлетворительным выполнение всех условий
        если ключ *, то оно ищется по всем полям"""
        if isinstance(value_dict, dict):
            result = True
            for key, value in value_dict.items():
                if key not in self.data:
                    if key == "*":
                        result = False
                        list_for_search = [str(x).lower().strip()
                                           for x in self.data.values()]
                        string = str(value).lower().strip()
                        if string in list_for_search:
                            result = True
                    else:
                        # print("Такого поля нет")
                        return None
                elif str(value).strip().lower() != self.data[key].lower().strip():
                    result = False
            return result
        raise NotDictionaryFormat


class ContactList():
    def __init__(self):
        self.data = {}
        self.start = -1

    def __eq__(self, other):
        return (self.data == other.data)

    def __getitem__(self, id):
        if id in self.data.keys():
            return self.data[id]

    def __iter__(self):
        return self

    def __next__(self):
        self.start += 1
        if self.start < len(self.data.items()):
            return list(self.data.items())[self.start]
        raise StopIteration

    @property
    def new_id(self):
        """Вычисляет новый id"""
        id = max(self.data.keys())+1 if self.data else 0
        return id

    def append_contact(self, contact: Contact, id=-1):
        """Добавляет контакт"""
        if id == -1:
            id = self.new_id
        if id in self.data.keys():
            raise NonUniqueId
        elif isinstance(contact, Contact):
            self.data[id] = contact
        else:
            raise CustomException(
                "Контакт не является объектом класса Contact")

    @classmethod
    def generate_random(cls, qty: int) -> 'ContactList':
        """Создает рандомные контакты"""
        new = cls()
        for _ in range(qty):
            new_contact = Contact.generate_random()
            new.append_contact(new_contact)
        return new

    @property
    def len_data(self) -> dict:
        """Вычисляет длину поля для печати"""
        id_len = len("id")
        len_data_dict = {}.fromkeys(CHECK_PATTERNS_DICT.keys(), 0)
        for id, contact in self.data.items():
            id_len = max(id_len, len(str(id)))
            len_data_dict.setdefault("id", id_len)
            for key, value in contact.len_data.items():
                len_data_dict[key] = max(value, len_data_dict[key])

        return len_data_dict

    def __str__(self):
        headers = ["id"]
        for key in CHECK_PATTERNS_DICT.keys():
            headers.append(f"{key:<{self.len_data[key]}}")
        print_str = ["| ".join(headers)]
        for id, contact in self.data.items():
            print_item = [f"{id:<{self.len_data['id']}}"]
            for key in CHECK_PATTERNS_DICT.keys():
                print_item.append(
                    f"{contact.data[key]:<{self.len_data[key]}}")
            print_str.append("| ".join(print_item))
        return "\n".join(print_str)+"\n"

    def find_id(self, value_dict: dict) -> list:
        """Ищет id контактов
        если передается словарь из имя поля:значение, то значение ищется в поле
        если в словаре несколько значений-условий, то считается удовлетворительным выполнение всех условий
        если ключ *, то ищется по всем полям"""
        id_list = []
        if value_dict:
            for id, contact in self.data.items():
                if value_dict.get("id") == id or contact.isfound(value_dict):
                    id_list.append(id)
        return id_list

    def filter(self, id_list: list) -> 'ContactList':
        """Фильтрует контакты по списку id"""
        filtered = ContactList()
        if id_list:
            for id in id_list:
                filtered.data[id] = self.data[id]
        return filtered

    def find(self, value_dict: dict) -> 'ContactList':
        """Находит контакты, которые соответствует данным из словаря value_dict"""
        id_list = self.find_id(value_dict)
        found = self.filter(id_list)
        return found

    def remove(self, value_dict: dict) -> 'ContactList':
        """Удаляет контакты, которые соответствует данным из словаря value_dict"""
        removed = ContactList()
        id_list = self.find_id(value_dict)
        if id_list:
            for id in id_list:
                removed.data[id] = self.data.pop(id)
        return removed

    def sort_contactlist(self) -> 'ContactList':
        """Сортирует данные по id"""
        self.data = dict(sorted(self.data.items()))
        return self


class ContactFile:
    def __init__(self, filename: str, option: str):
        self.filename = filename
        self.option = option
        self.file = None

    def __enter__(self):
        if self.option == "write":
            opt = "w"
        elif self.option == "read":  # если файл отсутствует, то создает его
            opt = "r"
            try:
                open(self.filename, opt, encoding='UTF-8')
            except:
                opt = "x"
        try:
            self.file = open(self.filename, opt, encoding='UTF-8')
            return self
        except FileNotFoundError:
            raise PhoneDataFileNotFoundError(self.filename)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.file:
            self.file.close()

    def csv_import(self) -> ContactList:
        """ Импортирует данные из файла csv в ContactList"""
        data = csv.DictReader(self.file, delimiter=',', quotechar='"')
        contact_list = ContactList()
        for item in list(data):
            """Здесь вставить исключение!!!"""
            id = int(item["id"])
            contact = Contact(*list(item.values())[1:])
            contact_list.append_contact(contact, id)
        return contact_list

    def csv_export(self, contact_list: ContactList):
        """ Экспортирует данные из ContactList и записывает в файл"""
        string = ",".join(HEADERS)+"\n"
        for id, contact in contact_list:
            string += str(id)
            for item in contact:
                string += ","+item[1]
            string += "\n"
        self.file.write(string)


class ContactListException:
    pass
