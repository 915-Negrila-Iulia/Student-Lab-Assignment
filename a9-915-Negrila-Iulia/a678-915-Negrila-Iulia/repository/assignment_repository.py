"""
Repository for assignment
"""
import datetime

from Iterable.iterable import Iterable
from domain.assignment import Assignment
from validator.validators import RepositoryException


class AssignmentRepository:
    def __init__(self, assignments_list=None):
        """
        Creates a list of assignments
        :param assignments_list: list of assignments
        """
        self._assignments_list = Iterable()
        if assignments_list is not None:
            self._assignments_list = assignments_list

    @property
    def assignments_list(self):
        """
        :return: the list of assignments
        """
        return self._assignments_list

    def add_assignment(self, new_assignment):
        """
        Adds a new assignment to the list of assignments
        :param new_assignment: the assignment which will be added to the list
        :return: -
        Raise RepositoryException if the id of the new assignment is the same as the
        id of an assignment from the list of assignments
        """
        for assignment in self._assignments_list:
            if assignment.entity_id == new_assignment.entity_id:
                raise RepositoryException('This id already exists')
        self._assignments_list.append(new_assignment)

    def remove_assignment(self, id_assignment):
        """
        Removes an assignment from the list of assignments by its id
        :param id_assignment: the id of the assignment which will be removed from the list
        :return: -
        """
        for assignment in self._assignments_list[:]:
            if assignment.entity_id == id_assignment:
                self._assignments_list.remove(assignment)
                return assignment

    def update_assignment(self, assignment, new_description, new_deadline):
        """

        :param student:
        :param new_description:
        :param new_deadline:
        :return:
        """
        old_description, old_deadline = assignment.description, assignment.deadline
        assignment.description = new_description
        assignment.deadline = new_deadline
        return assignment, old_description, old_deadline


