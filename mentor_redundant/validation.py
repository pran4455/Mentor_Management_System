from abc import ABC, abstractmethod
import re

# Strategy interfaces
class usernameValidationStrategy(ABC):
    @abstractmethod
    def validate(self, employee_id):
        pass

class PasswordValidationStrategy(ABC):
    @abstractmethod
    def validate(self, password):
        pass

# Concrete implementations of strategies
class RegexusernameValidation(usernameValidationStrategy):
    def validate(self,user_id):
        # Validate employee ID using regex
        return bool(re.match(r'^[a-zA-Z]+[0-9]{7}@ssn\.edu\.in$', user_id))

class RegexPasswordValidation(PasswordValidationStrategy):
    def validate(self, password):
        # Validate password using regex
        return bool(re.match(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[^\w\s]).{8,}$', password))

# Context class that uses the strategies
class ValidationContext:
    def __init__(self, strategy, data):
        self.strategy = strategy
        self.data = data

    def validate(self):
        return self.strategy.validate(self.data)

