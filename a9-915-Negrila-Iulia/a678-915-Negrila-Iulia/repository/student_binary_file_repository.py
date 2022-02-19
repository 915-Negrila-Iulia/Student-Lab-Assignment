import pickle

from repository.student_repository import StudentRepository


class StudentBinaryFileRepository(StudentRepository):
    """
    Inheritance
    StudentBinaryFileRepository 'is a' StudentRepository
    """
    def __init__(self, file_name):
        """
        Constructor for StudentBinaryFileRepository class
        :param file_name: name of the binary text
        """
        super().__init__()
        self._file_name = file_name
        self._students_list = self._load()

    def add_student(self, student):
        """
        Adds a student to the file by using the method of StudentRepository class
        :param student: student which is added
        :return: -
        """
        super().add_student(student)
        self._save(self._students_list)

    def remove_student(self, student_id):
        """
        Removes a student from the file by using the method of StudentRepository class
        :param student_id: id of the student which will be removed
        :return: -
        """
        super().remove_student(student_id)
        self._save(self._students_list)

    def update_student(self, student, new_name, new_group):
        """
        Changes the attributes of a student
        :param student: student which will be updated
        :param new_name: name which will replace the initial name of the student
        :param new_group: group which will replace the initial group of the student
        :return: -
        """
        super().update_student(student,new_name,new_group)
        self._save(self._students_list)

    def _load(self):
        """
        Reads from the binary file and adds students to the list of students
        :return: the list of students
        Raise IOError it there is an error
        """
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

    def _save(self, students):
        """
        Writes the students to the file in binary
        :param students: the list of students
        :return: -
        """
        file = open(self._file_name, "wb")
        pickle.dump(students, file)
        file.close()
