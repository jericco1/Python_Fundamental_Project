from abc import ABC, abstractmethod
import json
import random

class Bank(ABC):
    @abstractmethod
    def generate_account_number(self):
        pass

    @abstractmethod
    def read_data(self, data_file):
        pass

    @abstractmethod
    def write_data(self):
        pass

class SubBank(Bank):
    def __init__(self, data_file):
        self.data_file = data_file
        self.data = self.read_data(data_file)

    def generate_account_number(self):
        return random.randint(1000000000, 9999999999)

    def read_data(self, data_file):
        try:
            with open(data_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"users": [], "agents": []}

    def write_data(self):
        with open(self.data_file, 'w') as file:
            json.dump(self.data, file, ensure_ascii=False, indent=4)