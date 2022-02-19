import datetime

from domain.assignment import Assignment
from domain.grade import Grade
from domain.student import Student


class UndoRedoException(Exception):
    pass

class StudentException(Exception):
    """
    This is a costum exception class for student
    """

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message


class AssignmentException(Exception):
    """
    This is a costum exception class for assignment
    """

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message


class RepositoryException(Exception):
    """
    This is a costum exception class for repositories
    """

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message


class GradeException(Exception):
    """
    This is a costum exception class for grade
    """

    def __init__(self, message=''):
        self.message = message

    def __str__(self):
        return self.message


class StudentValidator:
    """
    Class for validating a student
    """

    @staticmethod
    def validate_student(student):
        if len(student.entity_id) == 0:
            raise StudentException('Empty value provided for id of student')
        if len(student.name) == 0:
            raise StudentException('Empty value provided for name of student')


class AssignmentValidator:
    """
    Class for validating an assignment
    """

    @staticmethod
    def validate_assignment(assignment):
        if len(assignment.entity_id) == 0:
            raise AssignmentException('Empty value provided for id of assignment')
        if len(assignment.description) == 0:
            raise AssignmentException('Empty value provided for description of assignment')


class GradeValidator:
    """
    Class for validating a grade
    """

    @staticmethod
    def validate_grade(grade):
        if grade is None:
            pass
        elif grade.grade_value is not None and (int(grade.grade_value) > 10 or int(grade.grade_value) < 1):
            raise GradeException('Grades must be between 1 and 10')


def test_student_validator():
    try:
        student_validator = StudentValidator()
        student = Student('', 'Zack', 911)
        student_validator.validate_student(student)
    except StudentException:
        assert True


def test_assignment_validator():
    try:
        assignment_validator = AssignmentValidator()
        assignment = Assignment('A2', '', datetime.datetime(2021, 2, 2))
        assignment_validator.validate_assignment(assignment)
    except AssignmentException:
        assert True


def test_grade_validator():
    try:
        grade_validator = GradeValidator()
        grade = Grade('111', 'A10', 100)
        grade_validator.validate_grade(grade)
    except GradeException:
        assert True
    grade_validator = GradeValidator()
    grade = Grade('111', 'A10')
    grade_validator.validate_grade(grade)
    assert grade.grade_value is None


test_student_validator()
test_assignment_validator()
test_grade_validator()
