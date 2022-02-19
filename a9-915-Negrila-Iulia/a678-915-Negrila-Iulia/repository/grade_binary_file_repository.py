
import pickle

from repository.grade_repository import GradeRepository


class GradeBinaryFileRepository(GradeRepository):
    def __init__(self, file_name):
        super().__init__()
        self._file_name = file_name
        self._grades_list = self._load()

    def add_grade(self, grade):
        super().add_grade(grade)
        self._save(self._grades_list)

    def remove_grade(self, student_id, assignment_id):
        super().remove_grade(student_id, assignment_id)
        self._save(self._grades_list)

    def update_grade(self, grade,new_grade_value):
        super().update_grade(grade,new_grade_value)
        self._save(self._grades_list)

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

    def _save(self, grades):
        file = open(self._file_name, "wb")
        pickle.dump(grades, file)
        file.close()


