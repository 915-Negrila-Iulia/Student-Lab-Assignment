import datetime
import unittest

from domain.assignment import Assignment
from domain.grade import Grade
from domain.student import Student
from repository.assignment_repository import AssignmentRepository
from repository.grade_repository import GradeRepository
from repository.student_repository import StudentRepository
from service.assignment_service import AssignmentService
from service.grade_service import GradeService
from service.student_service import StudentService
from validator.validators import StudentValidator, AssignmentValidator, GradeValidator


class TestStudentService(unittest.TestCase):

    def setUp(self):
        students_list = [Student('2Y122345', 'Rachel Green', 913), Student('3Y100000', 'Joey Tribbiani', 914),
                         Student('2Y115698', 'Chandler Bing', 915)]
        student_repository = StudentRepository(students_list)
        student_validator = StudentValidator()
        self._student_service = StudentService(student_repository, student_validator)

    def test_add_student(self):
        self._student_service.add_student('2Y111', 'Collin', 914)
        self.assertEqual(len(self._student_service.get_students()), 4)

    def test_remove_student(self):
        self._student_service.remove_student('2Y122345')
        self.assertEqual(len(self._student_service.get_students()), 2)

    def test_update_student(self):
        self._student_service.update_student('2Y122345', 'Just Rachel', 913)
        index_of_the_updated_student = 0
        updated_student_name = self._student_service.get_students()[index_of_the_updated_student].name
        updated_student_group = self._student_service.get_students()[index_of_the_updated_student].group
        self.assertEqual(updated_student_name, 'Just Rachel')
        self.assertEqual(updated_student_group, 913)


class TestAssignmentService(unittest.TestCase):

    def setUp(self):
        assignment_list = [Assignment('A1', 'Create a snake game', datetime.datetime(2020, 12, 20)),
                           Assignment('A2', 'Create a sudoku game', datetime.datetime(2021, 1, 23)),
                           Assignment('A3', 'Improve the snake game', datetime.datetime(2021, 2, 17))]
        assignment_repository = AssignmentRepository(assignment_list)
        assignment_validator = AssignmentValidator()
        self._assignment_service = AssignmentService(assignment_repository, assignment_validator)

    def test_add_assignment(self):
        self._assignment_service.add_assignment('A4', 'do undo/redo', datetime.datetime(2020, 12, 28))
        self.assertEqual(len(self._assignment_service.get_assignments()), 4)

    def test_remove_assignment(self):
        self._assignment_service.remove_assignment('A1')
        self.assertEqual(len(self._assignment_service.get_assignments()), 2)

    def test_update_assignment(self):
        self._assignment_service.update_assignment('A1', 'Create an app for a store', datetime.datetime(2020, 12, 28))
        index_of_the_updated_assignment = 0
        updated_assignment_description = \
            self._assignment_service.get_assignments()[index_of_the_updated_assignment].description
        updated_assignment_deadline = \
            self._assignment_service.get_assignments()[index_of_the_updated_assignment].deadline
        self.assertEqual(updated_assignment_description, 'Create an app for a store')
        self.assertEqual(updated_assignment_deadline, datetime.datetime(2020, 12, 28))


class TestGradeService(unittest.TestCase):

    def setUp(self):
        grade_list = [Grade('2Y122345', 'A1', 7), Grade('3Y100000', 'A1', 8), Grade('2Y122345', 'A2')]
        grade_repository = GradeRepository(grade_list)
        grade_validator = GradeValidator()
        students_list = [Student('2Y122345', 'Rachel Green', 913), Student('3Y100000', 'Joey Tribbiani', 915),
                         Student('2Y115698', 'Chandler Bing', 915)]
        students_repository = StudentRepository(students_list)
        assignments_list = [Assignment('A1', 'Create a snake game', datetime.datetime(2020, 12, 20)),
                            Assignment('A2', 'Create a sudoku game', datetime.datetime(2021, 1, 23)),
                            Assignment('A3', 'Improve the snake game', datetime.datetime(2021, 2, 17))]
        assignments_repository = AssignmentRepository(assignments_list)
        self._grade_service = GradeService(students_repository, assignments_repository, grade_repository,
                                           grade_validator)

    def test_give_assignment_to_student(self):
        self._grade_service.give_assignment_to_student('2Y115698', 'A1')
        self.assertEqual(len(self._grade_service.get_grades()), 4)

    def test_give_assignment_to_group_of_students(self):
        self._grade_service.give_assignment_to_group_of_students(915, 'A3')
        self.assertEqual(len(self._grade_service.get_grades()), 5)

    def test_get_list_of_ungraded_assignments_for_student(self):
        self._grade_service.give_grade_to_student_assignment('2Y122345', 'A2', 10)
        assignments_list = self._grade_service.get_list_of_ungraded_assignments_for_student('2Y122345')
        self.assertEqual(len(assignments_list), 0)

    def test_get_average_grade_of_assignment(self):
        sum_of_grades_of_assignment = 15
        number_of_grades_of_assignment = 2
        self.assertEqual(self._grade_service.get_average_grade_of_assignment('A1'),
                         float(sum_of_grades_of_assignment / number_of_grades_of_assignment))

