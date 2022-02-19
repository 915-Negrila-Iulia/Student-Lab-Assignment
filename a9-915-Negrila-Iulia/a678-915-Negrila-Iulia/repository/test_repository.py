import datetime
import unittest

from domain.assignment import Assignment
from domain.grade import Grade
from domain.student import Student
from repository.assignment_repository import AssignmentRepository
from repository.grade_repository import GradeRepository
from repository.student_repository import StudentRepository
from validator.validators import RepositoryException


class StudentRepositoryTest(unittest.TestCase):
    def setUp(self):
        students_list = [Student('2Y122345', 'Rachel Green', 913), Student('3Y100000', 'Joey Tribbiani', 914),
                         Student('2Y115698', 'Chandler Bing', 915)]
        self._students_repository = StudentRepository(students_list)

    def test_student_repository(self):
        self.assertEqual(len(self._students_repository.students_list), 3)

    def test_add_student(self):
        self._students_repository.add_student(Student('1Y785111', 'Ken', 915))
        self.assertEqual(len(self._students_repository.students_list), 4)
        self.assertEqual(self._students_repository.students_list[3].name, 'Ken')
        try:
            self._students_repository.add_student(Student('1Y785111', 'Lo', 915))
        except RepositoryException:
            assert True

    def test_remove_student(self):
        self._students_repository.remove_student('2Y122345')
        assert len(self._students_repository.students_list) == 2

    def test_find_student_by_id(self):
        student = self._students_repository.find_student_by_id('2Y122345')
        assert student.name == 'Rachel Green' and student.group == 913


class TestAssignmentRepository(unittest.TestCase):
    def setUp(self):
        assignments_list = [Assignment('A1', 'Create a snake game', datetime.datetime(2020, 12, 20)),
                            Assignment('A2', 'Create a sudoku game', datetime.datetime(2021, 1, 23)),
                            Assignment('A3', 'Improve the snake game', datetime.datetime(2021, 2, 17))]
        self._assignments_repository = AssignmentRepository(assignments_list)

    def test_assignment_repository(self):
        self.assertEqual(len(self._assignments_repository.assignments_list), 3)

    def test_add_assignment(self):
        self._assignments_repository.add_assignment(
            Assignment('A4', 'Do an undo function for sudoku game', datetime.datetime(2021, 4, 5)))
        self.assertEqual(len(self._assignments_repository.assignments_list), 4)
        try:
            self._assignments_repository.add_assignment(Assignment('A4', 'game', datetime.datetime(2021, 11, 5)))
        except RepositoryException:
            assert True

    def test_remove_assignment(self):
        self._assignments_repository.remove_assignment('A2')
        self.assertEqual(len(self._assignments_repository.assignments_list), 2)

    def test_find_assignment_by_id(self):
        assignment = self._assignments_repository.find_assignment_by_id('A3')
        self.assertEqual(assignment.description, 'Improve the snake game')
        self.assertEqual(assignment.deadline, datetime.datetime(2021, 2, 17))


class TestGradeRepository(unittest.TestCase):
    def setUp(self):
        grades_list = [Grade('Student1', 'Assignment1'), Grade('Student2', 'Assignment1', 8),
                       Grade('Student1', 'Assignment2')]
        self._grades_repository = GradeRepository(grades_list)

    def test_grade_repository(self):
        self.assertEqual(len(self._grades_repository.grades_list), 3)

    def test_add_grade(self):
        self._grades_repository.add_grade(Grade('Student2', 'Assignment3', 9))
        self.assertEqual(len(self._grades_repository.grades_list), 4)
        self._grades_repository.add_grade(Grade('Student1', 'Assignment1', 5))
        self.assertEqual(len(self._grades_repository.grades_list), 4)

    def test_find_grade_by_ids(self):
        grade = self._grades_repository.find_grade_by_ids('Student2', 'Assignment1')
        self.assertEqual(grade.grade_value, 8)

    def test_remove_grade(self):
        self._grades_repository.remove_grade('Student1', 'Assignment1')
        self.assertEqual(len(self._grades_repository.grades_list), 2)

