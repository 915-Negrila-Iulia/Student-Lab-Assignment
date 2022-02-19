"""
Repository for student
"""
from Iterable.iterable import Iterable
from domain.student import *
from validator.validators import RepositoryException


class StudentRepository:
    def __init__(self, students_list=None):
        """
        Creates a list of students
        :param students_list: the list of students
        """
        self._students_list = Iterable()
        if students_list is not None:
            self._students_list = students_list

    @property
    def students_list(self):
        """
        :return: the list of students
        """
        return self._students_list

    def add_student(self, new_student):
        """
        Adds a new student to the list of students
        :param new_student: the student who will be added to the list
        :return: -
        Raise RepositoryException if the id of the new student is the id of a student from the list of students
        """
        for student in self._students_list:
            if student.entity_id == new_student.entity_id:
                raise RepositoryException('This id already exists')
        self._students_list.append(new_student)

    def remove_student(self, student_id):
        """
        Removes a student from the list of students by its id
        :param student_id: the id of the student who will be removed from the list
        :return: -
        """
        for student in self._students_list[:]:
            if student.entity_id == student_id:
                self._students_list.remove(student)
                return student

    def update_student(self, student, new_name, new_group):
        """
        Change attributes of a student
        :param student:
        :param new_name:
        :param new_group:
        :return:
        """
        old_name, old_group = student.name, student.group
        student.name = new_name
        student.group = new_group
        return student, old_name, old_group
