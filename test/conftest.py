import os
import pytest
from copy import deepcopy
from ..src.controller.controller import MenuController
from ..src.model.model import ContactFile
from ..src.constants import HEADERS


@pytest.fixture(scope="class")
def mc():
    # создание тестового экземпляра
    test_phonebook='./data/test_data/phonebook.csv'
    mc = MenuController(test_phonebook)
    with ContactFile(mc.filename, "read") as phonebook:
        mc.contactlist = phonebook.csv_import()
        mc.old_contactlist = deepcopy(mc.contactlist)
    return mc

@pytest.fixture(scope="class")
def delete_nonexistent():
    # удаление тестового файла
    nonexistent="./data/test_data/phonebook_nonexistent.csv"
    if os.path.exists(nonexistent):
        os.remove(nonexistent)
    yield
    if os.path.exists(nonexistent):
        os.remove(nonexistent)

@pytest.fixture(scope="class")
def clear_saved():
    # очищение тествого файла 
    saved="./data/test_data/phonebook_saved.csv"
    os.remove(saved)
    with open(saved,"w") as file:
        file.write(",".join(HEADERS)+"\n")
    yield
    os.remove(saved)
    with open(saved,"w") as file:
        file.write(",".join(HEADERS)+"\n")