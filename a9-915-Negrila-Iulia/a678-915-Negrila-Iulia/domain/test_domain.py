import datetime
import unittest

from domain.assignment import Assignment
from domain.grade import Grade
from domain.student import Student


class StudentTest(unittest.TestCase):
    def test_student(self):
        student = Student('2Y122345', 'Kenny Joe', 913)
        self.assertEqual('2Y122345', student.entity_id)
        self.assertEqual('Kenny Joe', student.name)
        self.assertEqual(913, student.group)


class TestAssignment(unittest.TestCase):
    def test_assignment(self):
        assignment = Assignment('A1', 'Create a snake game', datetime.datetime(2020, 12, 20))
        self.assertEqual(assignment.entity_id, 'A1')
        self.assertEqual(assignment.description, 'Create a snake game')
        self.assertEqual(assignment.deadline, datetime.datetime(2020, 12, 20))


class TestGrade(unittest.TestCase):
    def test_grade(self):
        assignment = Assignment('A1', 'Create a snake game', datetime.datetime(2020, 12, 20))
        student = Student('2Y122345', 'Kenny Joe', 913)
        grade = Grade(student.entity_id, assignment.entity_id, 8)
        self.assertEqual(grade.assignment_id,'A1')
        self.assertEqual(grade.student_id,'2Y122345')
        self.assertEqual(grade.grade_value,8)

