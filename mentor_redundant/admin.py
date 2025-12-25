from mentee import Mentee
from mentor import Mentor
import json

'''
Singleton design pattern
is implemented here
'''
class admin:
    instance=None
    def __init__(self,username,password,Name,phno):
        if admin.instance==None:
            self.username=username
            self.password=password
            self.name=Name
            self.phno=phno
        admin.instance=self
    

if __name__ == '__main__':
    a = admin('piriyadharshini2210418@ssn.edu.in','Pdk164@#','piriyadharshini','8939155122')
    print(a.username)
    with open('users.json','w') as f1:
        json.dump({a.username:('admin',a.password)},f1)
    ''' # Add 5 mentors
    a.add_mentor('M1', 'Mentor1', '1234567890', 'mentor1@example.com', 'CSE', 'Mentor@123')
    a.add_mentor('M2', 'Mentor2', '2345678901', 'mentor2@example.com', 'IT', 'Mentor@456')
    a.add_mentor('M3', 'Mentor3', '3456789012', 'mentor3@example.com', 'ECE', 'Mentor@789')
    a.add_mentor('M4', 'Mentor4', '4567890123', 'mentor4@example.com', 'MECH', 'Mentor@987')
    a.add_mentor('M5', 'Mentor5', '5678901234', 'mentor5@example.com', 'EEE', 'Mentor@654')

    # Add 20 mentees
    a.add_mentee('S1', 'Mentee1', 9328429325, 'mentee1@example.com', 1, 'CSE', 'Mentee@123')
    a.add_mentee('S2', 'Mentee2', 9328429326, 'mentee2@example.com', 2, 'IT', 'Mentee@456')
    a.add_mentee('S3', 'Mentee3', 9328429327, 'mentee3@example.com', 3, 'ECE', 'Mentee@789')
    a.add_mentee('S4', 'Mentee4', 9328429328, 'mentee4@example.com', 4, 'MECH', 'Mentee@987')
    a.add_mentee('S5', 'Mentee5', 9328429329, 'mentee5@example.com', 5, 'EEE', 'Mentee@654')
    a.add_mentee('S6', 'Mentee6', 9328429330, 'mentee6@example.com', 1, 'CSE', 'Mentee@123')
    a.add_mentee('S7', 'Mentee7', 9328429331, 'mentee7@example.com', 2, 'IT', 'Mentee@456')
    a.add_mentee('S8', 'Mentee8', 9328429332, 'mentee8@example.com', 3, 'ECE', 'Mentee@789')
    a.add_mentee('S9', 'Mentee9', 9328429333, 'mentee9@example.com', 4, 'MECH', 'Mentee@987')
    a.add_mentee('S10', 'Mentee10', 9328429334, 'mentee10@example.com', 5, 'EEE', 'Mentee@654')
    a.add_mentee('S11', 'Mentee11', 9328429335, 'mentee11@example.com', 1, 'CSE', 'Mentee@123')
    a.add_mentee('S12', 'Mentee12', 9328429336, 'mentee12@example.com', 2, 'IT', 'Mentee@456')
    a.add_mentee('S13', 'Mentee13', 9328429337, 'mentee13@example.com', 3, 'ECE', 'Mentee@789')
    a.add_mentee('S14', 'Mentee14', 9328429338, 'mentee14@example.com', 4, 'MECH', 'Mentee@987')
    a.add_mentee('S15', 'Mentee15', 9328429339, 'mentee15@example.com', 5, 'EEE', 'Mentee@654')
    a.add_mentee('S16', 'Mentee16', 9328429340, 'mentee16@example.com', 1, 'CSE', 'Mentee@123')
    a.add_mentee('S17', 'Mentee17', 9328429341, 'mentee17@example.com', 2, 'IT', 'Mentee@456')
    a.add_mentee('S18', 'Mentee18', 9328429342, 'mentee18@example.com', 3, 'ECE', 'Mentee@789')
    a.add_mentee('S19', 'Mentee19', 9328429343, 'mentee19@example.com', 4, 'MECH', 'Mentee@987')
    a.add_mentee('S20', 'Mentee20', 9328429344, 'mentee20@example.com', 5, 'EEE', 'Mentee@654')
'''