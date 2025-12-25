class Meeting():
    def __init__(self):
        self.mentees=[]
        
    def add_requests(self,msg_name,body):
        self.alert_mentees(msg_name,body)
        
    def addMentee(self,mentee):
        self.mentees.append(mentee)
        
    def removeMenteementee(self, mentee):
        return self.mentees.remove(mentee)

    def alert_mentees(self,msg_name,body,username=None):
        for mentee in self.mentees:
            mentee.update(msg_name,body,username)