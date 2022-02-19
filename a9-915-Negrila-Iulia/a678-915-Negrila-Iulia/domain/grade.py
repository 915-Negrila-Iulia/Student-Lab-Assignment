from domain.assignment import *
from domain.student import *
import datetime


class Grade:
    """
        The class which represents a grade
    """

    def __init__(self, student_id, assignment_id, grade_value=None):
        """
        Constructor which creates a grade
        :param student_id: the id of the student which gets the grade (string type)
        :param assignment_id: the id of the assignment which is graded (string tye)
        :param grade_value: the value of the grade (integer between 1 and 10)
        """
        self._student_id = student_id
        self._assignment_id = assignment_id
        self._grade_value = grade_value

    @property
    def assignment_id(self):
        return self._assignment_id

    @property
    def student_id(self):
        return self._student_id

    @property
    def grade_value(self):
        return self._grade_value

    @grade_value.setter
    def grade_value(self, new_value_grade):
        self._grade_value = new_value_grade

    def __str__(self):
        return '( student id: ' + self._student_id + ', assignment id: ' + self._assignment_id + \
               ', grade: ' + str(self._grade_value) + ' )'


