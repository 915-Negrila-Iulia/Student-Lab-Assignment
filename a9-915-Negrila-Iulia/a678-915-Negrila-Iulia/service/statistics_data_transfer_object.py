class StudentGradeOfAssignment:
    """
    Data Transfer Object for statistics
    Move data between application layers
    """

    def __init__(self, student_name, grade_of_assignment):
        """
        The constructor of this class
        :param student_name: the student's name
        :param grade_of_assignment: the grade received by student for an assignment
        """
        self._student_name = student_name
        self._grade_of_assignment = grade_of_assignment

    @property
    def student_name(self):
        return self._student_name

    @property
    def grade_of_assignment(self):
        return self._grade_of_assignment

    def __str__(self):
        return self._student_name + ' - ' + str(self._grade_of_assignment)


class StudentDeadlineOfAssignment:
    """
    Data Transfer Object for statistics
    Move data between application layers
    """

    def __init__(self, student_id, student_name, assignment_id, deadline_of_assignment):
        """
        The constructor of this class
        :param student_id: the student's name
        :param student_name: the student's name
        :param assignment_id: the id of the assignment
        :param deadline_of_assignment: the date until an assignment must be done
        """
        self._student_id = student_id
        self._student_name = student_name
        self._assignment_id = assignment_id
        self._deadline_of_assignment = deadline_of_assignment

    @property
    def student_id(self):
        return self._student_id

    @property
    def student_name(self):
        return self._student_name

    @property
    def deadline_of_assignment(self):
        return self._deadline_of_assignment

    @property
    def assignment_id(self):
        return self._assignment_id

    def __str__(self):
        return self._student_id + ' ' + self._student_name + ' - ' + self._assignment_id + ' - ' +\
               str(self._deadline_of_assignment)


class StudentSchoolSituation:
    """
    Data Transfer Object for statistics
    Move data between application layers
    """

    def __init__(self, student_name, average_grade):
        """
        The constructor of this class
        :param student_name: the student's name
        :param average_grade: the average grade of all the grades of a student
        """
        self._student_name = student_name
        self._average_grade = average_grade

    @property
    def student_name(self):
        return self._student_name

    @property
    def average_grade(self):
        return self._average_grade

    def __str__(self):
        return self._student_name + ' - ' + str(self._average_grade)
