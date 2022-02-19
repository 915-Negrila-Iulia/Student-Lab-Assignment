from domain.grade import Grade
from repository.grade_repository import GradeRepository


class GradeTextFileRepository(GradeRepository):
    """
    Inheritance
    StudentTextFileRepository 'is a' StudentRepository
    """
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._load()

    def add_grade(self, grade):
        super().add_grade(grade)
        self._save()

    def remove_grade(self, student_id, assignment_id):
        super().remove_grade(student_id, assignment_id)
        self._save()

    def update_grade(self, grade, new_grade_value):
        super().update_grade(grade,new_grade_value)
        self._save()

    def _load(self):
        file = open(self._file_name, 'rt')
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.split(',')
            index_for_student_id = 0
            index_for_assignment_id = 1
            index_for_value_grade = 2

            try:
                super().add_grade(
                    Grade(line[index_for_student_id], line[index_for_assignment_id], int(line[index_for_value_grade])))
            except Exception:
                super().add_grade(Grade(line[index_for_student_id], line[index_for_assignment_id], None))

    def _save(self):
        file = open(self._file_name, 'wt')
        for grade in self.grades_list:
            line = grade.student_id + ',' + grade.assignment_id + ',' + str(grade.grade_value)
            file.write(line)
            file.write('\n')
        file.close()
