# import sys
# sys.path.append('...')

import pytest
from functools import wraps
from ..controller.controller import MenuController
from ..constants import CHECK_PATTERNS_DICT
from ..model.model import Contact
from ..model.exceptions import *


def input_value(*param):
    """Декоратор для замены ввода значений в терминале
        Вместо input() - *params"""
    def outer(func=None):
        @wraps(func)
        def inner(*args, **kwargs):
            if len(args) > 0:
                args = list(args)
                params = list(param)
                for i in range(1, len(params)+1):
                    args[i] = params[i]  # вместо input()
                return func(*tuple(args), **kwargs)
            else:
                return func(**kwargs)
        return inner
    return outer


"""
_________________________________________
print_all_data_main
_________________________________________
 """

expected_print_all_data_main_stdout = r"""
Результат:
id| surname | name     | phone         | comment 
0 | Федотова| Дарья    | +501 260946233| Белиз   
1 | Хромов  | Матвей   | +263 749056857| Зимбабве
2 | Борис   | Мирослава| +674 253348945| Науру   
3 | Федотова| Марина   | +501 267746233| Белиз   
4 | Федотов | Игорь    | +501 260946211| Белиз   
"""

expected_all = {
    0: {'surname': 'Федотова', 'name': 'Дарья', 'phone': '+501 260946233', 'comment': 'Белиз'},
    1: {'surname': 'Хромов', 'name': 'Матвей', 'phone': '+263 749056857', 'comment': 'Зимбабве'},
    2: {'surname': 'Борис', 'name': 'Мирослава', 'phone': '+674 253348945', 'comment': 'Науру'},
    3: {'surname': 'Федотова', 'name': 'Марина', 'phone': '+501 267746233', 'comment': 'Белиз'},
    4: {'surname': 'Федотов', 'name': 'Игорь', 'phone': '+501 260946211', 'comment': 'Белиз'}
}


def test_print_all_data_main_stdout(mc, capsys):
    """ Проверка корректности вывода на экран всех контактов"""
    mc.print_all_data_main()
    terminal_output = capsys.readouterr()
    output = expected_print_all_data_main_stdout[1:-1]
    assert terminal_output.out.strip("\n") == output


def test_print_all_data_main(mc):
    """Проверка загрузки данных из файла и корректности данных, передаваемых для отображения"""
    result = mc.print_all_data_main().data
    for key, value in result.items():
        result[key] = value.data
    assert result == expected_all


"""
_________________________________________
 remove_data_main
_________________________________________
 """

expected_remove_0 = {
    1: {'surname': 'Хромов', 'name': 'Матвей', 'phone': '+263 749056857', 'comment': 'Зимбабве'},
    2: {'surname': 'Борис', 'name': 'Мирослава', 'phone': '+674 253348945', 'comment': 'Науру'},
    3: {'surname': 'Федотова', 'name': 'Марина', 'phone': '+501 267746233', 'comment': 'Белиз'},
    4: {'surname': 'Федотов', 'name': 'Игорь', 'phone': '+501 260946211', 'comment': 'Белиз'}
}


@pytest.fixture(autouse=True)
def mock_input(monkeypatch):
    def mock_input(prompt):
        return "0"
    monkeypatch.setattr('builtins.input', mock_input)


def test_remove_data_main_terminal(mc, monkeypatch):
    """ Проверка удаления контакта по id
    Замена ввода с экрана с помощью monkeypatch"""
    mc.remove_data_main()
    result = mc.contactlist
    assert result == expected_remove_0


@pytest.mark.parametrize("value,expected", [
    ("0", expected_remove_0),  # удаление существующего контакта
    ("5", expected_all),  # удаление несуществующего контакта
    ("", expected_all),  # отсутствие вводимых данных
])
def test_remove_data_main_param(value, expected):
    """Параметризированный тест удаления контакта по id.
    Для замены input() применен декоратор @input_value"""
    @input_value(value)
    def test_remove_data_main(mc, expected):
        """ Проверка удаления контакта. Вместо ввода с экрана - декоратор, передающий значения
        Плюс parametrize - различные тесты """
        mc.remove_data_main()
        result = mc.contactlist
        assert result == expected


"""
_________________________________________
 append_data_main
_________________________________________
 """

expected_append_5 = {
    0: {'surname': 'Федотова', 'name': 'Дарья', 'phone': '+501 260946233', 'comment': 'Белиз'},
    1: {'surname': 'Хромов', 'name': 'Матвей', 'phone': '+263 749056857', 'comment': 'Зимбабве'},
    2: {'surname': 'Борис', 'name': 'Мирослава', 'phone': '+674 253348945', 'comment': 'Науру'},
    3: {'surname': 'Федотова', 'name': 'Марина', 'phone': '+501 267746233', 'comment': 'Белиз'},
    4: {'surname': 'Федотов', 'name': 'Игорь', 'phone': '+501 260946211', 'comment': 'Белиз'},
    5: {'surname': 'Крылышкин', 'name': 'Борис', 'phone': '123 456 789', 'comment': ''}}


@pytest.mark.parametrize("value,expected,hint", [
    (["Крылышкин", "Борис", "123 456 789", ""],
     expected_append_5, None),  # добавление контакта
    # добавление контакта Ввод фамилии пустой
    ([""], expected_all, CHECK_PATTERNS_DICT["surname"]["hint"]),
    (["123"], expected_append_5, CHECK_PATTERNS_DICT["surname"]
     ["hint"]),  # добавление контакта Ввод фамилии некорректный
    (["Крылышкин", ""], expected_append_5, CHECK_PATTERNS_DICT["name"]
     ["hint"]),  # добавление контакта Ввод имени пустой
    (["Крылышкин", "к3"], expected_append_5, CHECK_PATTERNS_DICT["name"]
     ["hint"]),  # добавление контакта Ввод имени некорректный
    (["Крылышкин", "Борис", ""], expected_append_5, CHECK_PATTERNS_DICT["phone"]
     ["hint"]),  # добавление контакта Ввод телефона пустой
    (["Крылышкин", "борис", "к3"], expected_append_5, CHECK_PATTERNS_DICT["phone"]
     ["hint"]),  # добавление контакта Ввод телефона некорректный
])
def test_append_data_main_param(value, expected, hint):
    """Параметризированный тест добавления контакта.
    Для замены input() применен декоратор @input_value"""
    @input_value(*value)
    def test_append_data_main(mc, expected, hint):
        """ Проверка удаления контакта. Вместо ввода с экрана - декоратор, передающий значения
        Плюс parametrize - различные тесты """
        try:
            mc.append_data_main()
            result = mc.contactlist
            assert result == expected
        except CustomException as e:
            assert str(e) == f"{hint}. Повторите ввод данных.\n"


"""
_________________________________________
find_data_main
_________________________________________
 """

expected_find_1 = {
    1: {'surname': 'Хромов', 'name': 'Матвей', 'phone': '+263 749056857', 'comment': 'Зимбабве'},
}
expected_find_25 = {
    2: {'surname': 'Борис', 'name': 'Мирослава', 'phone': '+674 253348945', 'comment': 'Науру'},
    5: {'surname': 'Крылышкин', 'name': 'Борис', 'phone': '123 456 789', 'comment': ''},
}
expected_none = {}


@pytest.mark.parametrize("value,expected", [
    (["1",], expected_find_1),  # поиск по id
    # поиск, если данные не введены
    (["", "", "", "", "", ""], expected_none),
    (["aaa",], expected_none),  # поиск по отсутствующему id
    # поиск по имени и фамилии
    (["", "Хромов", "Матвей", "", ""], expected_find_1),
    (["", "", "", "", "Борис"], expected_find_25),  # поиск по всем полям
])
def test_find_data_main_param(value, expected):
    """Параметризированный тест поиска контакта.
    Для замены input() применен декоратор @input_value"""
    @input_value(*value)
    def test_find_data_main(mc, expected):
        """ Проверка удаления контакта. Вместо ввода с экрана - декоратор, передающий значения
        Плюс parametrize - различные тесты """
        result = mc.find_data_main()
        assert result == expected


"""
_________________________________________
update_data_main
_________________________________________
 """

expected_update_none = {
    0: {'surname': 'Федотова', 'name': 'Дарья', 'phone': '+501 260946233', 'comment': 'Белиз'},
    1: {'surname': 'Хромов', 'name': 'Матвей', 'phone': '+263 749056857', 'comment': 'Зимбабве'},
    2: {'surname': 'Борис', 'name': 'Мирослава', 'phone': '+674 253348945', 'comment': 'Науру'},
    3: {'surname': 'Федотова', 'name': 'Марина', 'phone': '+501 267746233', 'comment': 'Белиз'},
    4: {'surname': 'Федотов', 'name': 'Игорь', 'phone': '+501 260946211', 'comment': 'Белиз'}
}
expected_update_0 = {
    0: {'surname': 'Федот', 'name': 'Михаил', 'phone': '123', 'comment': '-'},
    1: {'surname': 'Хромов', 'name': 'Матвей', 'phone': '+263 749056857', 'comment': 'Зимбабве'},
    2: {'surname': 'Борис', 'name': 'Мирослава', 'phone': '+674 253348945', 'comment': 'Науру'},
    3: {'surname': 'Федотова', 'name': 'Марина', 'phone': '+501 267746233', 'comment': 'Белиз'},
    4: {'surname': 'Федотов', 'name': 'Игорь', 'phone': '+501 260946211', 'comment': 'Белиз'}
}


@pytest.mark.parametrize("value,expected,hint", [
    (["0", "Федот", "Михаил", "aaa"], expected_update_none,
     CHECK_PATTERNS_DICT["phone"]),  # Изменение поля phone на некорректное
    ([""], expected_update_none, None),  # поиск, если id не введено
    # поиск, если id введено некорректно
    (["aaa"], expected_update_none, None),
    (["0", "Федот", "Михаил", "123", "-"],
     expected_update_0, None),  # изменение всех полей
])
def test_update_data_main_param(value, expected, hint):
    """Параметризированный тест изменения контакта.
    Для замены input() применен декоратор @input_value"""
    @input_value(*value)
    def test_update_data_main(mc, expected):
        """ Проверка изменения контакта. Вместо ввода с экрана - декоратор, передающий значения
        Плюс parametrize - различные тесты """
        try:
            mc.update_data_main()
            result = mc.contactlist
            assert result == expected
        except Exception as e:
            assert str(e) == f"{hint}. Повторите ввод данных.\n"


"""
_________________________________________
load_phonebook_data
_________________________________________
 """


@pytest.mark.parametrize("file_name,value,expected,hint", [
    # Открытие корректного файла
    ("./data/test_data/phonebook.csv", [], expected_all, None),
    ("./data/test_data/phonebook_empty.csv", [],
     expected_none, None),  # Открытие пустого файла
    ("./data/test_data/phonebook_headers.csv", [], None,
     f"В файле ./data/test_data/phonebook_headers.csv неверные заголовки"),  # Открытие файла с неверными заголовками
    # Открытие файла, с даными не удовлетворяющими условию уникальности id
    ("./data/test_data/phonebook_data.csv", [],
     None, f'id 0 не является целочисленным'),
    ("./data/test_data/phonebook_nonexistent.csv",
     ["n"], expected_none, ""),  # Открытие несуществующего файла
])
def test_load_phonebook_data_param(file_name, value, expected, hint):
    """Параметризированный тест загрузки данных из файла csv.
    Для замены input() применен декоратор @input_value"""
    @input_value(*value)
    def test_load_phonebook_data(file_name, value, expected, hint, delete_nonexistent):
        """Параметризированный тест загрузки данных из файла csv."""
        try:
            mc = MenuController(file_name)
            mc.load_phonebook_data()
            result = mc.contactlist
            assert result == expected
        except Exception as e:
            assert str(
                e) == f'{file_name} не соответствует требованиям: {hint}'


"""
_________________________________________
save_data_main
_________________________________________
 """
expected_filedata = """
id,surname,name,phone,comment
0,A,B,123,
"""


def test_save_data_main(clear_saved):
    """Параметризированный тест сохранения данных в файл csv."""
    testfile = "./data/test_data/phonebook_saved.csv"
    mc = MenuController(testfile)
    mc.load_phonebook_data()
    mc.contactlist.append_contact(Contact("A", "B", "123", ""))
    mc.save_data_main()
    with open(testfile, "r") as file:
        result = file.read()
    assert result == expected_filedata[1:]


"""
_________________________________________
quit_phonebook_main
_________________________________________
 """
expected_filedata_empty = """
id,surname,name,phone,comment
"""


@pytest.mark.parametrize("value,expected", [
    (["y"], expected_filedata),  # сохранение изменений
    (["n"], expected_filedata_empty),  # выход без сохранения изменений
])
def test_quit_phonebook_main_param(clear_saved, value, expected):
    """Параметризированный тест выхода"""
    @input_value(*value)
    def test_quit_phonebook_main(expected):
        testfile = "./data/test_data/phonebook_saved.csv"
        mc = MenuController(testfile)
        mc.load_phonebook_data()
        mc.contactlist.append_contact(Contact("A", "B", "123", ""))
        mc.quit_phonebook_main()
        with open(testfile, "r") as file:
            result = file.read()
        assert result == expected[1:]


if __name__ == "__main__":
    pytest.main(['-s', '-vv'])
