from domain.student import *
from repository.student_repository import StudentRepository
from service.undo_redo_service import FunctionCall, Operation
from validator.validators import StudentValidator, StudentException


class StudentService:
    """
    The non-Ui functionalities for the student class are here
    """

    def __init__(self, student_repository, student_validator, undo_redo_service):
        """
        The constructor of the StudentService
        :param student_repository: the repository for student
        :param student_validator: the validator for student
        :param undo_redo_service: the service for undo/redo operations
        """
        self._student_repository = student_repository
        self._student_validator = student_validator
        self._undo_redo_service = undo_redo_service

    def add_student(self, student_id, name, group):
        """
        Creates a student using the Student class
        Validates the student using a staticmethod of the StudentValidator class
        Adds the student to the list of students using a method implemented in the StudentRepository class
        Adds to the history of operations the undo and redo functions for add operation
        Creates Operations for undo and redo
        :param student_id: the id of the student who will be added (string type)
        :param name: the name of the student who will be added (string type)
        :param group: the group of the student who will be added (int type)
        :return: -
        Raise StudentException if the introduced values (id, name, group) are incorrect
        """
        student = Student(student_id, name, group)
        self._student_validator.validate_student(student)
        self._student_repository.add_student(student)

        undo_function = FunctionCall(self._student_repository.remove_student,student_id)
        redo_function = FunctionCall(self._student_repository.add_student, student)
        self._undo_redo_service.add_operation(Operation(undo_function,redo_function))


    def remove_student(self, student_id):
        """
        Removes a student by its id from the students list using a method implemented in the StudentRepository class
        Adds to the history of operations the undo and redo functions for remove operation
        Creates Operations for undo and redo
        :param student_id: the id of the student who will be removed
        :return: the operation created for undo/redo
        Raise StudentException if the id of student does not exist in the list of students
        """
        student = self.find_student_by_id(student_id)
        self._student_repository.remove_student(student_id)

        undo_function = FunctionCall(self._student_repository.add_student, student)
        redo_function = FunctionCall(self._student_repository.remove_student, student_id)
        return Operation(undo_function,redo_function)

    @property
    def get_students(self):
        """
        Using a property of the StudentRepository class, gets the list of students
        :return: the list with all the students
        """
        return self._student_repository.students_list

    def update_student_functionality(self, student_id, new_name, new_group):
        """
        Changes the attributes of a student (excepting the id)
        :param student_id: the id of the student whose attributes will be changed
        :param new_name: the name which will replace the previous name of the student
        :param new_group: the group which will replace the previous group of the student
        :return: the initial name and group of student (before replacing them with new_name and new_group)
        Raise StudentException if the id of student does not exist in the list of students
        """
        student = self.find_student_by_id(student_id)
        new_student, old_name, old_group = self._student_repository.update_student(student,new_name,new_group)

        self._student_validator.validate_student(new_student)
        return old_name, old_group

    def update_student(self, student_id, new_name, new_group):
        """
        Calls update_student_functionality method in order to change the attributes of a student
        Creates Operations for undo and redo
        :param student_id: the id of the student whose attributes will be changed
        :param new_name: the name which will replace the previous name of the student
        :param new_group: the group which will replace the previous group of the student
        :return: -
        """
        old_name, old_group = self.update_student_functionality(student_id, new_name, new_group)

        undo_function = FunctionCall(self.update_student_functionality, student_id, old_name, old_group)
        redo_function = FunctionCall(self.update_student_functionality, student_id, new_name, new_group)
        self._undo_redo_service.add_operation(Operation(undo_function,redo_function))

    def find_student_by_id(self, student_id):
        """
        Find a student from the list of students by its id
        :param student_id: the id given by the user, which will be compared with the ids of the students
        from the list of students
        :return: the student who has the id given by the user
        Raise RepositoryException if no student from the list of students has the id given by the user
        """
        for student in self._student_repository.students_list:
            if student_id == student.entity_id:
                return student
        raise StudentException('Student id not found')

    def find_group(self, group):
        """
        Find a group of students by its name
        :param group: name of the group
        :return: True if there is at least one student in this group and False otherwise
        """
        for student in self._student_repository.students_list:
            if student.group == group:
                return True
        return False

    def initialize_students(self):
        self._student_repository.add_student(Student('2Y122345', 'Rachel Green', 913))
        self._student_repository.add_student(Student('3Y100000', 'Joey Tribbiani', 914))
        self._student_repository.add_student(Student('2Y115698', 'Chandler Bing', 915))
        self._student_repository.add_student(Student('2Y115690', 'Alexa Bing', 915))
        self._student_repository.add_student(Student('1Y100345', 'Phoebe Buffay', 911))
        self._student_repository.add_student(Student('3Y185620', 'Tom', 911))
        self._student_repository.add_student(Student('1Y111299', 'Jerry', 912))
        self._student_repository.add_student(Student('2Y110000', 'Ken Green', 913))
        self._student_repository.add_student(Student('3Y124485', 'Collin Green', 913))
        self._student_repository.add_student(Student('1Y111230', 'James Adam', 914))