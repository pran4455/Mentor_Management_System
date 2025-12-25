from admin import admin
from mentee import Mentee
from mentor import Mentor
import random
from abc import ABC,abstractmethod

class AnyAllocationStrategy(ABC):
    @abstractmethod
    def allocate_mentor(self, mentee, mentors):
        pass
class deptAllocationStrategy(ABC):
    @abstractmethod
    def allocate_mentor(self, mentee, mentors):
        pass

class AnyMentorAllocationStrategy(AnyAllocationStrategy):
    def allocate_mentor(self, mentee, mentors):
        # Filter mentors whose mentee list is less than 20
        eligible_mentors = [mentor for mentor in mentors if len(mentor.mentees) < 20]
        return random.choice(eligible_mentors) if eligible_mentors else None

class DepartmentMentorAllocationStrategy(deptAllocationStrategy):
    def allocate_mentor(self, mentee, mentors):
        mentee_department = mentee.get_department()
        eligible_mentors = [mentor for mentor in mentors if mentor.get_department() == mentee_department]

        # Filter mentors whose mentee list is less than 20
        eligible_mentors = [mentor for mentor in eligible_mentors if len(mentor.mentees) < 20]

        return random.choice(eligible_mentors) if eligible_mentors else None

# Mentor and Mentee classes
# Context class that uses the strategies
class allocationContext:
    def __init__(self, strategy,mentee,mentors):
        self.strategy = strategy
        self.mentee = mentee
        self.mentor=mentors

    def allocate_mentor(self):
        return self.strategy.allocate_mentor(self.mentee,self.mentor)
