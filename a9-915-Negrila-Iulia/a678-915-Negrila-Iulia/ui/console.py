import datetime

from domain.student import Student
from repository.assignment_binary_file_repository import AssignmentBinaryFileRepository
from repository.assignment_repository import AssignmentRepository
from repository.assignment_text_file_repository import AssignmentTextFileRepository
from repository.grade_binary_file_repository import GradeBinaryFileRepository
from repository.grade_repository import GradeRepository
from repository.grade_text_file_repository import GradeTextFileRepository
from repository.student_binary_file_repository import StudentBinaryFileRepository
from repository.student_repository import StudentRepository
from repository.student_text_file_repository import StudentTextFileRepository
from service.assignment_service import AssignmentService
from service.grade_service import GradeService
from service.settings_properties import SettingsProperties
from service.student_service import StudentService
from service.undo_redo_service import UndoRedoService
from validator.validators import StudentValidator, AssignmentValidator, GradeValidator


class Console:
    """
    This class handles the Ui functions
    """

    def __init__(self, student_service, assignment_service, grade_service, undo_redo_service):
        """
        Constructor for Console class
        :param student_service: the service for student
        :param assignment_service: the service for assignment
        :param grade_service: the service for grade
        :param undo_redo_service: the service for undo/redo operations
        """
        self._student_service = student_service
        self._assignment_service = assignment_service
        self._grade_service = grade_service
        self._undo_redo_service = undo_redo_service

    def ui_display_students(self):
        for student in self._student_service.get_students:
            print(student)

    def ui_add_student(self):
        student_id = input('id student: ')
        name = input('name: ')
        group = int(input('group: '))
        self._student_service.add_student(student_id, name, group)

    def ui_remove_student(self):
        student_id = input('id student: ')
        self._grade_service.remove_assignments_of_student(student_id)

    def ui_update_student(self):
        student_id = input('id student: ')
        new_name = input('give new name: ')
        new_group = int(input('give new group: '))
        self._student_service.update_student(student_id, new_name, new_group)

    def ui_display_assignments(self):
        for assignment in self._assignment_service.get_assignments:
            print(assignment)

    def ui_add_assignment(self):
        assignment_id = input('id assignment: ')
        description = input('description: ')
        """
        year = int(input('year for deadline: '))
        month = int(input('month for deadline: '))
        day = int(input('day for deadline: '))
        deadline = datetime.datetime(year,month,day)
        """
        deadline = input('deadline (year/month/day): ')
        year, month, day = self.split_deadline_command(deadline)
        deadline = datetime.datetime(year, month, day)
        self._assignment_service.add_assignment(assignment_id, description, deadline)

    def split_deadline_command(self, deadline):
        """
        Splits the deadline given by user in year month and day
        :param deadline: command given by user which represents the deadline of an assignment
        :return: year month and day of the deadline
        """
        deadline = deadline.strip().split('/')
        index_of_year_from_deadline = 0
        index_of_month_from_deadline = 1
        index_of_day_from_deadline = 2
        year = int(deadline[index_of_year_from_deadline])
        month = int(deadline[index_of_month_from_deadline])
        day = int(deadline[index_of_day_from_deadline])
        return year, month, day

    def ui_remove_assignment(self):
        assignment_id = input('id assignment: ')
        self._grade_service.remove_grades_of_assignment(assignment_id)

    def ui_update_assignment(self):
        assignment_id = input('id assignment: ')
        new_description = input('give new description: ')
        new_deadline = input('give new deadline (year/month/day): ')
        new_year, new_month, new_day = self.split_deadline_command(new_deadline)
        new_deadline = datetime.datetime(new_year, new_month, new_day)
        self._assignment_service.update_assignment(assignment_id, new_description, new_deadline)

    def ui_give_assignment_to_student(self):
        student_id = input('give student id: ')
        assignment_id = input('give assignment id: ')
        self._grade_service.give_assignment_to_student(student_id, assignment_id)

    def ui_give_assignment_to_group_of_students(self):
        group = int(input('give group: '))
        assignment_id = input('give assignment id: ')
        self._grade_service.give_assignment_to_group_of_students(group, assignment_id)

    def display_grades(self):
        for grade in self._grade_service.get_grades():
            print(grade)

    def display_list_of_ungraded_assignments(self, student_id):
        for assigment_id in self._grade_service.get_list_of_ungraded_assignments_for_student(student_id):
            print(assigment_id)

    def ui_give_grade_to_student_assignment(self):
        student_id = input('give student id: ')
        print(f'List of ungraded assignments of {student_id} student:')
        self.display_list_of_ungraded_assignments(student_id)
        assignment_id = input('give assignment id: ')
        new_value_grade = int(input('give grade: '))
        self._grade_service.give_grade_to_student_assignment(student_id, assignment_id, new_value_grade)

    def ui_students_ordered_by_average_grade_of_assignment(self):
        assignment_id = input('give assignment id: ')
        ordered_list = self._grade_service.order_students_by_average_grade_of_assignment(assignment_id)
        average_grade = self._grade_service.get_average_grade_of_assignment(assignment_id)
        print(f'the average grade of {assignment_id} is {average_grade}')
        for student in ordered_list:
            print(student)

    def ui_students_late_in_handling_assignments(self):
        students_late_in_handling_assignments_list = self._grade_service.students_late_in_handling_assignments()
        for student in students_late_in_handling_assignments_list:
            print(student)

    def ui_sort_students_by_average_grades(self):
        sorted_students_by_average_grades_list = self._grade_service.sort_students_by_average_grades()
        for student in sorted_students_by_average_grades_list:
            print(student)

    def ui_undo(self):
        self._undo_redo_service.undo()

    def ui_redo(self):
        self._undo_redo_service.redo()

    def print_menu(self):
        print()
        print('hi!')
        print('0: exit')
        print('1: adds new student')
        print('2: removes one student')
        print('3: display all students')
        print('4: update student')
        print('5: adds new assignment')
        print('6: removes one assignment')
        print('7: display all assignments')
        print('8: update assignment')
        print('9: give an assignment to a student')
        print('10: give an assignment to a group of students')
        print('11: display students and their assignments')
        print("12: give a grade to a student's assignment")
        print('13: display students ordered by the average grade of an assignment')
        print('14: students who are late in handling at least one assignment')
        print('15: students with the best school situation')
        print('16: undo')
        print('17: redo')
        print()

    def initialize(self):

        self._student_service.initialize_students()

        self._assignment_service.initialize_assignments()

        self._grade_service.initialize_grades()

    def start_menu(self):
        #self.initialize()
        done = False
        while not done:
            #try:
                self.print_menu()
                option = input('please enter option: ')
                if option == '1':
                    self.ui_add_student()
                elif option == '2':
                    self.ui_remove_student()
                elif option == '3':
                    self.ui_display_students()
                elif option == '4':
                    self.ui_update_student()
                elif option == '5':
                    self.ui_add_assignment()
                elif option == '6':
                    self.ui_remove_assignment()
                elif option == '7':
                    self.ui_display_assignments()
                elif option == '8':
                    self.ui_update_assignment()
                elif option == '9':
                    self.ui_give_assignment_to_student()
                elif option == '10':
                    self.ui_give_assignment_to_group_of_students()
                elif option == '11':
                    self.display_grades()
                elif option == '12':
                    self.ui_give_grade_to_student_assignment()
                elif option == '13':
                    self.ui_students_ordered_by_average_grade_of_assignment()
                elif option == '14':
                    self.ui_students_late_in_handling_assignments()
                elif option == '15':
                    self.ui_sort_students_by_average_grades()
                elif option == '16':
                    self.ui_undo()
                elif option == '17':
                    self.ui_redo()
                elif option == '0':
                    done = True
                    print('bye!')
                else:
                    print('incorrect option')
            #except Exception as exception:
            #   print(str(exception))

settings_properties = SettingsProperties()
dictionary = settings_properties.settings_data

if dictionary["repository"] == "inmemory":
    student_repository = StudentRepository()
    assignment_repository = AssignmentRepository()
    grade_repository = GradeRepository()

elif dictionary["repository"] == "textfiles":
    student_repository = StudentTextFileRepository(dictionary["students"])
    assignment_repository = AssignmentTextFileRepository(dictionary["assignments"])
    grade_repository = GradeTextFileRepository(dictionary["grades"])

elif dictionary["repository"] == "binaryfiles":
    student_repository = StudentBinaryFileRepository(dictionary["students"])
    assignment_repository = AssignmentBinaryFileRepository(dictionary["assignments"])
    grade_repository = GradeBinaryFileRepository(dictionary["grades"])


student_validator = StudentValidator()

undo_redo_service = UndoRedoService()
student_service = StudentService(student_repository, student_validator, undo_redo_service)
assignment_validator = AssignmentValidator()
assignment_service = AssignmentService(assignment_repository, assignment_validator, undo_redo_service)
grade_validator = GradeValidator()
grade_service = GradeService(grade_repository, grade_validator,
                             undo_redo_service, student_service, assignment_service)
ui_console = Console(student_service, assignment_service, grade_service, undo_redo_service)
ui_console.start_menu()

