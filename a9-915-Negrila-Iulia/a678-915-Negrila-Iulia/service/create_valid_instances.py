from domain.student import Student


class ValidStudent:
    """
    Create validated instances of Ingredient
    """

    def __init__(self, validator):
        self._validator = validator

    def create_student(self, student_id, name, group):
        student = Student(student_id, name, group)
        self._validator.validate_student(student)
        return student