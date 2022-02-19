import pickle

from repository.assignment_repository import AssignmentRepository
from repository.student_repository import StudentRepository


class AssignmentBinaryFileRepository(AssignmentRepository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._assignments_list = self._load()

    def add_assignment(self, assignment):
        super().add_assignment(assignment)
        self._save(self._assignments_list)

    def remove_assignment(self, assignment_id):
        super().remove_assignment(assignment_id)
        self._save(self._assignments_list)

    def update_assignment(self, assignment, new_description, new_deadline):
        super().update_assignment(assignment,new_description,new_deadline)
        self._save(self._assignments_list)

    def _load(self):
        try:
            file = open(self._file_name, 'rb')
            lines = pickle.load(file)
            file.close()
            return lines
        except EOFError:
            return []
        except IOError as error:
            print("An error occured - " + str(error))
            raise error

    def _save(self, assignments):
        file = open(self._file_name, "wb")
        pickle.dump(assignments, file)
        file.close()
