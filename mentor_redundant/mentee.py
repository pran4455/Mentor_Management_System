# Concrete Component
from quickstart import *

class Mentee:
    def __init__(self,username,password,names, contact_number,year, department):
        self.username = username
        self.password = password
        self.names=names
        self.contact_number = contact_number
        self.year = year
        self.department = department
        self.currentmentor=None 
        self.pastmentor=[] # Mentor assigned to the mentee
    
    def get_year(self):
        return self.year

    def get_department(self):
        return self.department
    
    def update(self,msg_name,body,username=None):
        if username==None:
            send_message(service,self.username,msg_name,body)
        else:
            send_message(service,username,msg_name,body)





