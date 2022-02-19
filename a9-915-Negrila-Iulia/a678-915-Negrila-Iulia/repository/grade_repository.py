"""
Repository for Grade
"""
from Iterable.iterable import Iterable
from domain.grade import Grade
from validator.validators import RepositoryException


class GradeRepository:
    def __init__(self, grades_list=None):
        """
        Creates a list of grades
        :param grades_list: the list of grades
        """
        self._grades_list = Iterable()
        if grades_list is not None:
            self._grades_list = grades_list

    @property
    def grades_list(self):
        """
        :return: list of grades
        """
        return self._grades_list

    def add_grade(self, new_grade):
        """
        Adds a new grade to the list of grades (so a student gets an assignment)
        If the student already has the assignment he will not get it again
        :param new_grade: the grade which will be added to the list
        :return: -
        """
        student_has_this_assignment = False
        for grade in self._grades_list:
            if grade.student_id == new_grade.student_id and grade.assignment_id == new_grade.assignment_id:
                student_has_this_assignment = True
        if not student_has_this_assignment:
            self._grades_list.append(new_grade)

    def find_grade_by_ids(self, student_id, assignment_id):
        """
        Find a grade from the list of grades by its student id and assignment id
        :param student_id: the id of student given by the user, which will be compared with the ids
        of the students from the list of grades
        :param assignment_id: the id of assignment given by the user, which will be compared with the ids of
        the assignments from the list of grades
        :return: the grade which has the ids (for student and for assignment) given by the user
        Raise RepositoryException if one of the given ids does not exist in the lists
        """
        for grade in self._grades_list:
            if grade.student_id == student_id and grade.assignment_id == assignment_id:
                return grade
        raise RepositoryException('student id or assignment id not found')


    def remove_grade(self, student_id, assignment_id):
        """
        Removes a grade from the list of grades by its ids (student id and assigment id)
        :param student_id: the id of the student whose grade will be removed from the list of grades
        :param assignment_id: the id of the assigment of the student whose grade will be removed from the list of grades
        :return: -
        """
        for grade in self._grades_list[:]:
            if grade.student_id == student_id and grade.assignment_id == assignment_id:
                self._grades_list.remove(grade)
                return grade

    def update_grade(self,grade, new_value_grade):
        grade.grade_value = new_value_grade
        return grade