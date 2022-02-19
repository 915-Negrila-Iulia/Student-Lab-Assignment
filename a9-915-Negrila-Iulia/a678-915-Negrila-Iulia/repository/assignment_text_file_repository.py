import datetime

from domain.assignment import Assignment
from repository.assignment_repository import AssignmentRepository


class AssignmentTextFileRepository(AssignmentRepository):

    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add_assignment(self, assignment):
        super().add_assignment(assignment)
        self._save()

    def remove_assignment(self, assignment_id):
        super().remove_assignment(assignment_id)
        self._save()

    def update_assignment(self, assignment, new_description, new_deadline):
        super().update_assignment(assignment,new_description,new_deadline)
        self._save()

    def _load(self):
        file = open(self._file_name, 'rt')
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.split(',')
            index_for_id = 0
            index_for_description= 1
            index_for_deadline = 2
            year,month,day = line[index_for_deadline].split('-')
            super().add_assignment(
                Assignment(line[index_for_id], line[index_for_description], datetime.datetime(year=int(year),month=int(month),day=int(day))))

    def _save(self):
        file = open(self._file_name, 'wt')
        for assignment in self.assignments_list:
            line = assignment.entity_id + ',' + assignment.description + ',' + str(assignment.deadline).split(' ')[0]
            file.write(line)
            file.write('\n')
        file.close()

