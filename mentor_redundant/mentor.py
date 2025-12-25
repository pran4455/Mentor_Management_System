from catmark import *
class Mentor:
    def __init__(self,username,password, names, contact_number,department):
        self.username = username
        self.password=password
        self.names = names
        self.contact_number = contact_number
        self.department = department 
        self.mentees=[]
        self.control=self.invoker()

    def get_department(self):
        return self.department

    def add_mentee(self, mentee):
        if len(self.mentees) < 20:
            self.mentees.append(mentee)
            return True
        else:
            return False
         
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "names": self.names,
            "contact_number": self.contact_number,
            "department": self.department,
            "mentees": [mentee.to_dict() for mentee in self.mentees]
        }

    def invoker(self):
        mentee_button = MenteeButton()
        enable_command = EnableButtonCommand(mentee_button)
        disable_command = DisableButtonCommand(mentee_button)
        return Invoker(enable_command,disable_command)