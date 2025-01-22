class RandomDataFileNotFoundError(Exception):
    def __init__(self, filename):
        self.filename = filename
        super().__init__(f"File not found: {filename}")

class PhoneDataFileNotFoundError(Exception):
    def __init__(self, filename):
        self.filename = filename
        super().__init__(f"File not found: {filename}")

class FieldNotFound(Exception):
    def __init__(self, key):
        self.key = key
    
    def __str__(self):
        return f'Поле {self.key} отсутствует'
    
class NotDictionaryFormat(Exception):
    def __init__(self, value_dict):
        self.value_dict = value_dict
    
    def __str__(self):
        return f'Передан формат, отличный от словаря {self.value_dict}'
    
class NonUniqueId(Exception):
    def __init__(self, id):
        self.id = id
    
    def __str__(self):
        return f'Id {id} не соответствует требованию уникальности'
    
class CustomException(Exception):
    def __init__(self, message):
        self.message=message
        super().__init__(message)
