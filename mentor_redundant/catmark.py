from meeting import *
# Command Interface
class Command:
    def execute(self):
        pass

# Concrete Command for Enabling
class EnableButtonCommand(Command):
    def __init__(self, mentee_button):
        self.mentee_button = mentee_button#Invoker.enable_command.mentee_button.is_enabled()
                                          #mentor.control.enable_command.mentee_button.is_enabled()
    def execute(self):
        self.mentee_button.enable()

# Concrete Command for Disabling
class DisableButtonCommand(Command):
    def __init__(self, mentee_button):
        self.mentee_button = mentee_button

    def execute(self):
        self.mentee_button.disable()

# Receiver
class MenteeButton:
    def __init__(self):
        self.enabled = False

    def enable(self):
        self.enabled = True
        print("Mentee button is now enabled.")

    def disable(self):
        self.enabled = False
        print("Mentee button is now disabled.")
    
    def is_enabled(self):
        return self.enabled

# Invoker
class Invoker:
    def __init__(self, enable_command, disable_command):
        self.enable_command = enable_command
        self.disable_command = disable_command

    def send_email(self,mentees,msg):
        # Simulate sending an email to all mentees
        print('inside send_email')
        send=Meeting()
        for i in mentees:
            send.addMentee(i)
        send.alert_mentees('SEM GPA COLLECTION',msg)

        print("Email sent to all mentees.")

        # Enable the mentee button
        self.enable_command.execute()
        return self

    def disable_button(self):
        # Disable the mentee button
        self.disable_command.execute()
        return self
