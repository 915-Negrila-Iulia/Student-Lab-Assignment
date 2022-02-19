from domain.assignment import *
from repository.assignment_repository import AssignmentRepository
from service.undo_redo_service import FunctionCall, Operation
from validator.validators import AssignmentValidator, AssignmentException


class AssignmentService:
    def __init__(self, assignment_repository, assignment_validator, undo_redo_service):
        self._assignment_repository = assignment_repository
        self._assignment_validator = assignment_validator
        self._undo_redo_service = undo_redo_service

    def add_assignment(self, assignment_id, description, deadline):
        """
        Creates an assignment using the assignment class
        Validates the assignment using a staticmethod of the validator assignment class
        Adds the assignment to the list of assignments using a method implemented in the assignment repository class
        Creates Operations for undo and redo
        :param assignment_id: the id of the assignment who will be added
        :param description: the description of the assignment who will be added
        :param deadline: the deadline of the assignment who will be added
        :return: -
        """
        assignment = Assignment(assignment_id, description, deadline)
        self._assignment_validator.validate_assignment(assignment)
        self._assignment_repository.add_assignment(assignment)

        undo_function = FunctionCall(self._assignment_repository.remove_assignment, assignment_id)
        redo_function = FunctionCall(self._assignment_repository.add_assignment, assignment)
        self._undo_redo_service.add_operation(Operation(undo_function, redo_function))

    def remove_assignment(self, assignment_id):
        """
        Removes an assignment by its id from the assignments list using a method implemented
        in the assignment repository class
        Creates Operations for undo and redo
        :param assignment_id: the id of the assignment who will be removed
        :return: the operation created for undo/redo
        Raise AssignmentException f the id of assignment does not exist in the list of assignments
        """
        assignment = self.find_assignment_by_id(assignment_id)
        self._assignment_repository.remove_assignment(assignment_id)

        undo_function = FunctionCall(self._assignment_repository.add_assignment, assignment)
        redo_function = FunctionCall(self._assignment_repository.remove_assignment, assignment_id)
        return Operation(undo_function, redo_function)

    @property
    def get_assignments(self):
        """
        Using a property of the AssignmentRepository class, gets the list of assignments
        :return: the list with all the assignments
        """
        return self._assignment_repository.assignments_list

    def update_assignment_functionality(self, assignment_id, new_description, new_deadline):
        """
        Changes the attributes of an assignment (excepting the id)
        :param assignment_id: the id of the assignment whose attributes will be changed
        :param new_description: the description which will replace the previous description of the assignment
        :param new_deadline: the deadline which will replace the previous deadline of the assignment
        :return: the initial description and deadline on an assignment
        Raise AssignmentException if the id of assignment does not exist in the list of assignments
        """
        assignment = self.find_assignment_by_id(assignment_id)
        new_assignment, old_description, old_deadline = \
            self._assignment_repository.update_assignment(assignment, new_description, new_deadline)
        self._assignment_validator.validate_assignment(new_assignment)
        return old_description, old_deadline

    def update_assignment(self, assignment_id, new_description, new_deadline):
        """
        Calls update_assignment_functionality method in order to change the attributes on an assignment
        Creates Operations for undo and redo
        :param assignment_id: the id of the assignment whose attributes will be changed
        :param new_description: the description which will replace the previous description of the assignment
        :param new_deadline: the deadline which will replace the previous deadline of the assignment
        :return: -
        """
        old_description, old_deadline = self.update_assignment_functionality(assignment_id, new_description, new_deadline)

        undo_function = FunctionCall(self.update_assignment_functionality, assignment_id, old_description, old_deadline)
        redo_function = FunctionCall(self.update_assignment_functionality, assignment_id, new_description, new_deadline)
        self._undo_redo_service.add_operation(Operation(undo_function, redo_function))


    def find_assignment_by_id(self, assignment_id):
        """
        Find an assignment from the list of assignments by its id
        :param assignment_id: the id given by the user, which will be compared with the ids of the assignments
        from the list of assignments
        :return: the assignment which has the id given by the user
        Raise RepositoryException if no assignment from the list of assignments has the id given by the user
        """
        for assignment in self._assignment_repository.assignments_list:
            if assignment_id == assignment.entity_id:
                return assignment
        raise AssignmentException('Assignment id not found')

    def initialize_assignments(self):
        self._assignment_repository.add_assignment(Assignment('A1', 'Create a snake game', datetime.datetime(2020, 12, 20)))
        self._assignment_repository.add_assignment(Assignment('A2', 'Create a sudoku game', datetime.datetime(2020, 1, 23)))
        self._assignment_repository.add_assignment(Assignment('A3', 'Improve the snake game', datetime.datetime(2020, 2, 17)))
        self._assignment_repository.add_assignment(Assignment('A4', 'Create an app like googlemaps', datetime.datetime(2021, 2, 20)))
        self._assignment_repository.add_assignment(Assignment('A5', 'Create an calculator app', datetime.datetime(2020, 3, 15)))
        self._assignment_repository.add_assignment(Assignment('A6', 'Improve the googlemaps app', datetime.datetime(2020, 3, 26)))
        self._assignment_repository.add_assignment(Assignment('A7', 'Improve the calculator app', datetime.datetime(2021, 4, 5)))
        self._assignment_repository.add_assignment(Assignment('A8', 'Do undo/redo for calculator app', datetime.datetime(2021, 4, 20)))
        self._assignment_repository.add_assignment(Assignment('A9', 'Create a website', datetime.datetime(2020, 5, 10)))
        self._assignment_repository.add_assignment(Assignment('A10', 'Improve the website', datetime.datetime(2021, 5, 17)))