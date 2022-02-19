from domain.student import Student
from repository.student_repository import StudentRepository
from service.create_valid_instances import ValidStudent
from validator.validators import StudentValidator


class StudentTextFileRepository(StudentRepository):
    """
    Inheritance
    StudentTextFileRepository 'is a' StudentRepository
    """
    def __init__(self, file_name):
        """
        Constructor for StudentTextFileRepository class
        :param file_name: name of the text
        """
        super().__init__()
        self._file_name = file_name
        self._load()

    def add_student(self, student):
        """
        Adds a student to the file by using the method of StudentRepository class
        :param student: student which is added
        :return: -
        """
        super().add_student(student)
        self._save()

    def remove_student(self, student_id):
        """
        Removes a student from the file by using the method of StudentRepository class
        :param student_id: id of the student which will be removed
        :return: -
        """
        super().remove_student(student_id)
        self._save()

    def update_student(self, student, new_name, new_group):
        """
        Changes the attributes of a student
        :param student: student which will be updated
        :param new_name: name which will replace the initial name of the student
        :param new_group: group which will replace the initial group of the student
        :return: -
        """
        super().update_student(student,new_name,new_group)
        self._save()

    def _load(self):
        """
        Reads line by line from the file text and adds students to the list of students
        :return: -
        """
        file = open(self._file_name, 'rt')
        lines = file.readlines()
        file.close()

        for line in lines:
            line = line.split(',')
            index_for_id = 0
            index_for_name = 1
            index_for_group = 2
            super().add_student(Student(line[index_for_id], line[index_for_name], int(line[index_for_group])))

    def _save(self):
        """
        Writes the students to the file
        :return: -
        """
        file = open(self._file_name, 'wt')
        for student in self.students_list:
            line = student.entity_id + ',' + student.name + ',' + str(student.group)
            file.write(line)
            file.write('\n')
        file.close()
