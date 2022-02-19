import datetime

from Iterable.iterable import Iterable
from domain.grade import Grade
from service.statistics_data_transfer_object import StudentGradeOfAssignment, StudentDeadlineOfAssignment, \
    StudentSchoolSituation
from service.undo_redo_service import FunctionCall, Operation, CascadedOperation
from validator.validators import GradeException, StudentException


class GradeService:
    """
    The non-Ui functionalities for the grade class are here
    """

    def __init__(self, grade_repository, grade_validator, undo_redo_service,
                 student_service, assignment_service):
        """
        The constructor of the GradeService class
        :param student_service: service for student
        :param assignment_service: service for assignment
        :param grade_repository: repository for grade
        :param grade_validator: validator for grade
        """
        self._grade_repository = grade_repository
        self._grade_validator = grade_validator
        self._undo_redo_service = undo_redo_service
        self._student_service = student_service
        self._assignment_service = assignment_service

    def give_assignment_to_student_handler(self, student_id, assignment_id):
        """
        Adds a new grade to the list of grades which represents an assignment given to a student
        If the student id given by the user does not belong to any student in the list of students or
        if the assignment id  given by the user does not belong to any assignment in the list of assignments
        no grade will be added to the list of grades
        :param student_id: id of the student who will get the assignment (it is given by the user)
        :param assignment_id: id of the assignment which will be given to a student (it is given by the user)
        :return: the grade which is added to the list of grades
        """
        grade = Grade(student_id, assignment_id)
        if self._student_service.find_student_by_id(student_id) and \
                self._assignment_service.find_assignment_by_id(assignment_id):
            self._grade_validator.validate_grade(grade)
            self._grade_repository.add_grade(grade)

        return grade

    def give_assignment_to_student(self, student_id, assignment_id):
        """
        Calls give_assignment_to_student_handler in order to add a new grade to the list of grades
        which represents an assignment given to a student
        Creates Operations for undo and redo
        :param student_id: id of the student who will get the assignment (it is given by the user)
        :param assignment_id: id of the assignment which will be given to a student (it is given by the user)
        :return: -
        """
        grade = self.give_assignment_to_student_handler(student_id, assignment_id)

        undo_function = FunctionCall(self._grade_repository.remove_grade, student_id, assignment_id)
        redo_function = FunctionCall(self._grade_repository.add_grade, grade)
        self._undo_redo_service.add_operation(Operation(undo_function, redo_function))

    def give_assignment_to_group_of_students(self, group, assignment_id):
        """
        Adds a new grade to the list of grades (which represents an assignment given to a student)
        for every student who belongs to the group introduced by the user
        Creates CascadedOperation for multiple undo and redo
        :param group: the group of students who will get the assignment
        :param assignment_id: the assignment which will be given to a group of students
        :return: -
        Raise StudentException if no student is in the group given by the user
        """
        cascade_list = []
        if self._student_service.find_group(group) is True:
            for student in self._student_service.get_students:
                if student.group == group:
                    grade = self.give_assignment_to_student_handler(student.entity_id, assignment_id)
                    undo_function = FunctionCall(self._grade_repository.remove_grade, student.entity_id, assignment_id)
                    redo_function = FunctionCall(self._grade_repository.add_grade, grade)
                    cascade_list.append(Operation(undo_function, redo_function))
            cascaded_operation = CascadedOperation(*cascade_list)
            self._undo_redo_service.add_operation(cascaded_operation)
        else:
            raise StudentException('This group does not exist')

    def get_list_of_ungraded_assignments_for_student(self, student_id):
        """
        Check in the list of grades the ungraded assignments for a student
        and create a list with this assignments ids
        :param student_id: id of the student given by the user who has the assignments this method searches for
        :return: the list of assignments of the student which has the student id given
        and which value of grade is None
        """
        ungraded_assignments_list = []
        for grade in self._grade_repository.grades_list:
            if grade.student_id == student_id and grade.grade_value is None:
                ungraded_assignments_list.append(grade.assignment_id)
        return ungraded_assignments_list

    def give_grade_to_student_assignment_handler(self, student_id, assignment_id, new_value_grade):
        """
        Change the None value of a grade of student's assignment with a new value
        :param student_id: the id of the student whose assignment will be graded
        :param assignment_id: the id of the assignment which will be graded
        :param new_value_grade: the value of the grade for the student's assignment (integer type)
        :return: grade which has the student id and assignment id given by the user
        Raise GradeError if the value of the grade which is replaced is not None (so an assignment can not pe graded twice)
        Raise GradeError if the new value of the grade is not between 1 and 10
        """

        ungraded_assignments_list = self.get_list_of_ungraded_assignments_for_student(student_id)
        grade = self._grade_repository.find_grade_by_ids(student_id, assignment_id)
        assignment_is_ungraded = False

        for id_assignment in ungraded_assignments_list:
            if id_assignment == assignment_id:
                assignment_is_ungraded = True

        if not assignment_is_ungraded:
            raise GradeException('An assignment can not be graded twice')
        else:
            new_grade = self._grade_repository.update_grade(grade, new_value_grade)
            self._grade_validator.validate_grade(new_grade)

        return grade

    def undo_give_grade_to_student_assignment(self, grade):
        """
        Set grade value to None
        :param grade: grade which value will be deleted
        :return: -
        """
        grade.grade_value = None

    def give_grade_to_student_assignment(self, student_id, assignment_id, new_value_grade):
        """
        Calls give_grade_to_student_assignment_handler method in order to grade a student's assignment
        :param student_id: the id of the student whose assignment will be graded
        :param assignment_id: the id of the assignment which will be graded
        :param new_value_grade: the value of the grade for the student's assignment (integer type)
        Creates Operations for undo and redo
        :return: -
        """
        grade = self.give_grade_to_student_assignment_handler(student_id, assignment_id, new_value_grade)

        undo_function = FunctionCall(self.undo_give_grade_to_student_assignment, grade)
        redo_function = FunctionCall(self.give_grade_to_student_assignment_handler, student_id, assignment_id,
                                     new_value_grade)

        self._undo_redo_service.add_operation(Operation(undo_function, redo_function))

    def get_grades(self):
        """
        :return: the list of grades
        """
        return self._grade_repository.grades_list

    def get_length(self):
        """
        :return: the length of the list of grades
        """
        return len(self.get_grades())

    def remove_assignments_of_student(self, student_id):
        """
        Removes all the grades of a student from the list of grades
        Creates CascadedOperation for multiple undo and redo
        :param student_id: the id of the student whose grades will be removed
        :return: -
        """
        cascade_list = []
        operation = self._student_service.remove_student(student_id)
        cascade_list.append(operation)
        for grade in self._grade_repository.grades_list[:]:
            if grade.student_id == student_id:
                self._grade_repository.remove_grade(student_id, grade.assignment_id)
                undo_function = FunctionCall(self._grade_repository.add_grade,
                                             Grade(student_id, grade.assignment_id, grade.grade_value))
                redo_function = FunctionCall(self._grade_repository.remove_grade, student_id, grade.assignment_id)
                cascade_list.append(Operation(undo_function, redo_function))
        cascaded_operation = CascadedOperation(*cascade_list)
        self._undo_redo_service.add_operation(cascaded_operation)

    def remove_grades_of_assignment(self, assignment_id):
        """
        Removes the grades of students of one assignment (from the list of grades)
        Creates CascadedOperation for multiple undo and redo
        :param assignment_id: the id of the assignment for which grades will be removed
        :return: -
        """
        cascade_list = []
        operation = self._assignment_service.remove_assignment(assignment_id)
        cascade_list.append(operation)
        for grade in self._grade_repository.grades_list[:]:
            if grade.assignment_id == assignment_id:
                self._grade_repository.remove_grade(grade.student_id, assignment_id)
                undo_function = FunctionCall(self._grade_repository.add_grade,
                                             Grade(grade.student_id, assignment_id, grade.grade_value))
                redo_function = FunctionCall(self._grade_repository.remove_grade, grade.student_id, assignment_id)
                cascade_list.append(Operation(undo_function, redo_function))
        cascaded_operation = CascadedOperation(*cascade_list)
        self._undo_redo_service.add_operation(cascaded_operation)

    def get_average_grade_of_assignment(self, assignment_id):
        """
        Computes the average grade of all the grades of one assignment
        :param assignment_id: the id of the assignment given by the user
        :return: the average grade of the grades of one assignment
        Raise GradeException if there is not any grade for this assignment
        """
        average_grade = 0
        number_of_students_with_given_assignment = 0

        for assignment_grade in self._grade_repository.grades_list:
            if assignment_grade.assignment_id == assignment_id and assignment_grade.grade_value is not None:
                average_grade += assignment_grade.grade_value
                number_of_students_with_given_assignment += 1

        if number_of_students_with_given_assignment == 0:
            raise GradeException(f'No student has assignment {assignment_id}')

        average_grade = float(average_grade / number_of_students_with_given_assignment)
        return average_grade

    def order_students_by_average_grade_of_assignment(self, assignment_id):
        """
        Creates a list which contains students who received this assignment ordered by the average grade of assignment
        :param assignment_id: the assignment given by the user
        :return: the list of students and their grades ordered by the average grade of a given assignment
        """

        ordered_students_by_grades_list = []

        greater_than_average = self.list_of_students_with_grades_greater_than_average(assignment_id)
        equal_to_average = self.list_of_students_with_grades_equal_to_average(assignment_id)
        less_than_average = self.list_of_students_with_grades_less_than_average(assignment_id)
        grade_value_is_none = self.list_of_students_with_no_grade(assignment_id)

        ordered_students_by_grades_list.extend(greater_than_average)
        ordered_students_by_grades_list.extend(equal_to_average)
        ordered_students_by_grades_list.extend(less_than_average)
        ordered_students_by_grades_list.extend(grade_value_is_none)

        return ordered_students_by_grades_list

    def get_average_grade_for_student(self, student_id):
        """
        Computes the average grade of all the grades of one student
        :param student_id: the id of the student whose average grade will be computed
        :return: the average grade of grades received by a student (float type)
        """
        average_grade = 0
        number_of_graded_assignments = 0

        for grade in self._grade_repository.grades_list:
            if grade.student_id == student_id and grade.grade_value is not None:
                average_grade += grade.grade_value
                number_of_graded_assignments += 1

        if number_of_graded_assignments == 0:
            average_grade = 0
            return average_grade

        average_grade = float(average_grade / number_of_graded_assignments)
        return average_grade

    def list_of_students_with_grades_greater_than_average(self, assignment_id):
        """
        Creates list for students whose grades are greater than the average grade of this assignment
        :param assignment_id: the assignment given by the user
        :return: the list of students with grade greater than the average one
        """
        greater_than_average = Iterable()
        average_grade_of_assignment = self.get_average_grade_of_assignment(assignment_id)

        for grade in self._grade_repository.grades_list:
            if grade.assignment_id == assignment_id:
                student = self._student_service.find_student_by_id(grade.student_id)
                greater_than_average.append(StudentGradeOfAssignment(student.name, grade.grade_value))

        greater_than_average.filter(lambda student: student.grade_of_assignment is not None and
                                                    student.grade_of_assignment > average_grade_of_assignment)
        return greater_than_average

    def list_of_students_with_grades_equal_to_average(self, assignment_id):
        """
        Creates list for students whose grades are equal to the average grade of this assignment
        :param assignment_id: the assignment given by the user
        :return: the list of students with grade equal to the average one
        """
        equal_to_average = Iterable()
        average_grade_of_assignment = self.get_average_grade_of_assignment(assignment_id)

        for grade in self._grade_repository.grades_list:
            if grade.assignment_id == assignment_id:
                student = self._student_service.find_student_by_id(grade.student_id)
                equal_to_average.append(StudentGradeOfAssignment(student.name, grade.grade_value))

        equal_to_average.filter(lambda student: student.grade_of_assignment is not None and
                                                student.grade_of_assignment == average_grade_of_assignment)
        return equal_to_average

    def list_of_students_with_grades_less_than_average(self, assignment_id):
        """
        Creates list for students whose grades are less than the average grade of this assignment
        :param assignment_id: the assignment given by the user
        :return: the list of students with grade less than the average one
        """
        less_than_average = Iterable()
        average_grade_of_assignment = self.get_average_grade_of_assignment(assignment_id)

        for grade in self._grade_repository.grades_list:
            if grade.assignment_id == assignment_id:
                student = self._student_service.find_student_by_id(grade.student_id)
                less_than_average.append(StudentGradeOfAssignment(student.name, grade.grade_value))

        less_than_average.filter(lambda student: student.grade_of_assignment is not None and
                                                 student.grade_of_assignment < average_grade_of_assignment)
        return less_than_average

    def list_of_students_with_no_grade(self, assignment_id):
        """
        Creates a list with students received this assignment but do not have a grade for it
        :param assignment_id: the assignment given by the user
        :return: the list of students who do not have a grade for this assignment
        """
        grade_value_is_none = Iterable()

        for grade in self._grade_repository.grades_list:
            if grade.assignment_id == assignment_id:
                student = self._student_service.find_student_by_id(grade.student_id)
                grade_value_is_none.append(StudentGradeOfAssignment(student.name, grade.grade_value))

        grade_value_is_none.filter(lambda student: student.grade_of_assignment is None)
        return grade_value_is_none

    def students_late_in_handling_assignments(self):
        """
        Checks for each student from the students list if at least one of their assignments (which passed their deadline)
        is not graded
        Creates a list for this students which contains their name, the id and the deadline for one of the assignments
        which were not handled on time
        :return: list of students who are late in handling at least one of their assignments
        """
        students_late_in_handling_assignments_list = Iterable()

        for student in self._student_service.get_students:
            ungraded_assignments_list = self.get_list_of_ungraded_assignments_for_student(student.entity_id)
            for assignment_id in ungraded_assignments_list:
                assignment = self._assignment_service.find_assignment_by_id(assignment_id)
                students_late_in_handling_assignments_list.append(
                    StudentDeadlineOfAssignment(student.entity_id, student.name, assignment.entity_id,
                                                assignment.deadline))

        students_late_in_handling_assignments_list.filter(
            lambda student: student.deadline_of_assignment < datetime.datetime.now())

        return students_late_in_handling_assignments_list

    def sort_students_by_average_grades(self):
        """
        Create a new list (iterable data type) which contains all the students from the list of students
        Sort the new list of students by their average grade using shell_sort method of the Iterable class
        :return: the sorted list of students
        """
        sorted_students_by_average_grades_list = Iterable()
        for student in self._student_service.get_students:
            sorted_students_by_average_grades_list.append(
                StudentSchoolSituation(student.name, self.get_average_grade_for_student(student.entity_id)))

        sorted_students_by_average_grades_list.shell_sort(lambda student1, student2:
                                                          student1.average_grade > student2.average_grade)
        return sorted_students_by_average_grades_list



    def sort_students_by_average_grades1(self):
        """
        Create a new list which contains all the students from the list of students
        Sort the new list of students by their average grade
        :return: the sorted list of students
        """
        sorted_students_by_average_grades_list = []

        for student in self._student_service.get_students:
            sorted_students_by_average_grades_list.append(
                StudentSchoolSituation(student.name, self.get_average_grade_for_student(student.entity_id)))
        sorted_students_by_average_grades_list.sort(key=lambda student_situation: student_situation.average_grade,
                                                    reverse=True)

        return sorted_students_by_average_grades_list

    def students_late_in_handling_assignments1(self):
        """
        Checks for each student from the students list if at least one of their assignments (which passed their deadline)
        is not graded
        Creates a list for this students which contains their name, the id and the deadline for one of the assignments
        which were not handled on time
        :return: list of students who are late in handling at least one of their assignments
        """

        students_late_in_handling_assignments_list = []

        for student in self._student_service.get_students:
            ungraded_assignments_list = self.get_list_of_ungraded_assignments_for_student(student.entity_id)
            for assignment_id in ungraded_assignments_list:
                assignment = self._assignment_service.find_assignment_by_id(assignment_id)
                if assignment.deadline < datetime.datetime.now():
                    students_late_in_handling_assignments_list.append(
                        StudentDeadlineOfAssignment(student.entity_id,student.name, assignment.entity_id, assignment.deadline))
                    break

        return students_late_in_handling_assignments_list

    def list_of_students_with_grades_greater_than_average1(self, assignment_id):
        """
        Creates list for students whose grades are greater than the average grade of this assignment
        :param assignment_id: the assignment given by the user
        :return: the list of students with grade greater than the average one
        """
        greater_than_average = []
        average_grade_of_assignment = self.get_average_grade_of_assignment(assignment_id)

        for grade in self._grade_repository.grades_list:
            if grade.assignment_id == assignment_id:
                student = self._student_service.find_student_by_id(grade.student_id)
                if grade.grade_value is not None and grade.grade_value > average_grade_of_assignment:
                    greater_than_average.append(StudentGradeOfAssignment(student.name, grade.grade_value))

        return greater_than_average

    def list_of_students_with_grades_equal_to_average1(self, assignment_id):
        """
        Creates list for students whose grades are equal to the average grade of this assignment
        :param assignment_id: the assignment given by the user
        :return: the list of students with grade equal to the average one
        """
        equal_to_average = []
        average_grade_of_assignment = self.get_average_grade_of_assignment(assignment_id)

        for grade in self._grade_repository.grades_list:
            if grade.assignment_id == assignment_id:
                student = self._student_service.find_student_by_id(grade.student_id)
                if grade.grade_value is not None and grade.grade_value == average_grade_of_assignment:
                    equal_to_average.append(StudentGradeOfAssignment(student.name, grade.grade_value))

        return equal_to_average

    def list_of_students_with_grades_less_than_average1(self, assignment_id):
        """
        Creates list for students whose grades are less than the average grade of this assignment
        :param assignment_id: the assignment given by the user
        :return: the list of students with grade less than the average one
        """
        less_than_average = []
        average_grade_of_assignment = self.get_average_grade_of_assignment(assignment_id)

        for grade in self._grade_repository.grades_list:
            if grade.assignment_id == assignment_id:
                student = self._student_service.find_student_by_id(grade.student_id)
                if grade.grade_value is not None and grade.grade_value < average_grade_of_assignment:
                    less_than_average.append(StudentGradeOfAssignment(student.name, grade.grade_value))

        return less_than_average

    def list_of_students_with_no_grade1(self, assignment_id):
        """
        Creates a list with students received this assignment but do not have a grade for it
        :param assignment_id: the assignment given by the user
        :return: the list of students who do not have a grade for this assignment
        """
        grade_value_is_none = []

        for grade in self._grade_repository.grades_list:
            if grade.assignment_id == assignment_id:
                student = self._student_service.find_student_by_id(grade.student_id)
                if grade.grade_value is None:
                    grade_value_is_none.append(StudentGradeOfAssignment(student.name, grade.grade_value))

        return grade_value_is_none

    def initialize_grades(self):

        self._grade_repository.add_grade(Grade('2Y122345', 'A2', None))
        self._grade_repository.add_grade(Grade('2Y122345', 'A1', 8))
        self._grade_repository.add_grade(Grade('2Y115698', 'A1', 10))
        self._grade_repository.add_grade(Grade('2Y115690', 'A1', 8))
        self._grade_repository.add_grade(Grade('2Y110000', 'A1', 9))
        self._grade_repository.add_grade(Grade('3Y124485', 'A1', 10))
        self._grade_repository.add_grade(Grade('2Y115698', 'A2', None))
        self._grade_repository.add_grade(Grade('2Y115690', 'A2', None))
        self._grade_repository.add_grade(Grade('2Y110000', 'A2', 9))
        self._grade_repository.add_grade(Grade('3Y124485', 'A2', 7))
        self._grade_repository.add_grade(Grade('1Y100345', 'A1', None))
        self._grade_repository.add_grade(Grade('3Y185620', 'A1', 7))
        self._grade_repository.add_grade(Grade('3Y124485', 'A3', 9))