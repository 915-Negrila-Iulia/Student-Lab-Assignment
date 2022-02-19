import sys
from PyQt5 import QtWidgets, uic
import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QListWidget, QVBoxLayout, QLineEdit, QPushButton, QComboBox

from repository.assignment_repository import AssignmentRepository
from repository.assignment_text_file_repository import AssignmentTextFileRepository
from repository.grade_repository import GradeRepository
from repository.grade_text_file_repository import GradeTextFileRepository
from repository.student_repository import StudentRepository
from repository.student_text_file_repository import StudentTextFileRepository
from service.assignment_service import AssignmentService
from service.grade_service import GradeService
from service.settings_properties import SettingsProperties
from service.student_service import StudentService
from service.undo_redo_service import UndoRedoService
from validator.validators import StudentValidator, AssignmentValidator, GradeValidator


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        student_validator = StudentValidator()

        student_repository = StudentTextFileRepository("D:/An1 Sem1/A homework FP/a10-915-Negrila-Iulia-main/a9-915"
                                                       "-Negrila-Iulia/a678-915-Negrila-Iulia/ui/students.txt")
        assignment_repository = AssignmentTextFileRepository("D:/An1 Sem1/A homework "
                                                             "FP/a10-915-Negrila-Iulia-main/a9-915-Negrila-Iulia/a678"
                                                             "-915-Negrila-Iulia/ui/assignments.txt")
        grade_repository = GradeTextFileRepository("D:/An1 Sem1/A homework FP/a10-915-Negrila-Iulia-main/a9-915"
                                                   "-Negrila-Iulia/a678-915-Negrila-Iulia/ui/grades.txt")

        undo_redo_service = UndoRedoService()
        student_service = StudentService(student_repository, student_validator, undo_redo_service)
        assignment_validator = AssignmentValidator()
        assignment_service = AssignmentService(assignment_repository, assignment_validator, undo_redo_service)
        grade_validator = GradeValidator()
        grade_service = GradeService(grade_repository, grade_validator,
                                     undo_redo_service, student_service, assignment_service)
        self._student_service = student_service
        self._assignment_service = assignment_service
        self._grade_service = grade_service
        self._undo_redo_service = undo_redo_service

        # Load the UI Page
        uic.loadUi('mainwindow.ui', self)
        self.set_up()
        self.connect_signals_and_slots()

    def refresh_students_list(self):
        self.dataList.clear()
        for stud in self._student_service.get_students:
            self.dataList.addItem(str(stud))

    def refresh_assignments_list(self):
        self.dataList.clear()
        for assignment in self._assignment_service.get_assignments:
            self.dataList.addItem(str(assignment))

    def refresh_data_list(self):
        current_text = self.StudAssigComboBox.currentText()
        if current_text == "Students":
            self.refresh_students_list()
            self.set_text_lines("student id","name","group")
        elif current_text == "Assignments":
            self.refresh_assignments_list()
            self.set_text_lines("assignment id","description","date(year/month/day)")
        else:
            self.dataList.clear()
            self.clear_text_lines()

    def set_up(self):
        self.displayList.setCurrentRow(0)
        self.refresh_data_list()

    def add_data_list(self):
        current_text = self.StudAssigComboBox.currentText()
        if current_text == "Students":
            self.add_student()
        elif current_text == "Assignments":
            self.add_assignment()
        self.clear_text_lines()

    def clear_text_lines(self):
        self.idText.clear()
        self.nameDescrText.clear()
        self.groupDateText.clear()

    def set_text_lines(self, line1, line2, line3):
        self.idText.setText(line1)
        self.nameDescrText.setText(line2)
        self.groupDateText.setText(line3)

    def add_student(self):
        student_id = self.idText.text()
        name = self.nameDescrText.text()
        group = int(self.groupDateText.text())
        try:
            self._student_service.add_student(student_id, name, group)
        except Exception as e:
            self.QMessageBox.critical(self, "Error", e)                ###does not work###
        self.refresh_students_list()

    def add_assignment(self):
        assignment_id = self.idText.text()
        description = self.nameDescrText.text()
        deadline = self.groupDateText.text()
        year, month, day = self.split_deadline_command(deadline)
        deadline = datetime.datetime(year, month, day)
        self._assignment_service.add_assignment(assignment_id, description, deadline)
        self.refresh_assignments_list()

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

    def update_text_lines(self):
        row = int(self.dataList.currentRow())
        i=0
        current_text = self.StudAssigComboBox.currentText()
        if current_text == "Students":
            for stud in self._student_service.get_students:
                if i == row:
                    self.set_text_lines(stud.entity_id,stud.name,str(stud.group))
                i+=1
        elif current_text == "Assignments":
            for assign in self._assignment_service.get_assignments:
                if i == row:
                    deadline = str(assign.deadline)
                    deadline = deadline.split(' ')[0]
                    deadline = deadline.replace('-','/')
                    self.set_text_lines(assign.entity_id,assign.description,deadline)
                i+=1

    def remove_data_list(self):
        current_text = self.StudAssigComboBox.currentText()
        if current_text == "Students":
            self.remove_student()
        elif current_text == "Assignments":
            self.remove_assignment()
        self.clear_text_lines()

    def remove_student(self):
        student_id = self.idText.text()
        try:
            self._grade_service.remove_assignments_of_student(student_id)
        except Exception as e:
            print(str(e))
        self.refresh_students_list()

    def remove_assignment(self):
        assignment_id = self.idText.text()
        self._grade_service.remove_grades_of_assignment(assignment_id)
        self.refresh_assignments_list()

    def update_data_list(self):
        row = int(self.dataList.currentRow())
        i = 0
        current_text = self.StudAssigComboBox.currentText()
        if current_text == "Students":
            for stud in self._student_service.get_students:
                if i == row:
                    try:
                        self.update_student(stud.entity_id)
                    except: pass
                i += 1
        elif current_text == "Assignments":
            for assign in self._assignment_service.get_assignments:
                if i == row:
                    try:
                        self.update_assignment(assign.entity_id)
                    except: pass
                i += 1
        self.refresh_data_list()

    def update_student(self, id):
        new_name = self.nameDescrText.text()
        new_group = int(self.groupDateText.text())
        self._student_service.update_student(id, new_name, new_group)

    def update_assignment(self, id):
        new_description = self.nameDescrText.text()
        deadline = self.groupDateText.text()
        year, month, day = self.split_deadline_command(deadline)
        new_deadline = datetime.datetime(year, month, day)
        self._assignment_service.update_assignment(id, new_description, new_deadline)

    def display_data(self):
        row = int(self.displayList.currentRow())
        display_data_list = []
        if row == 0:
            for grade in self._grade_service.get_grades():
                display_data_list.append(grade)
            self.sub_window = SubWindow("Students and their Assignments",display_data_list)
        elif row == 1:
            assignment_id = self._assignment_service.get_assignments[0].entity_id
            row = int(self.dataList.currentRow())
            i = 0
            current_text = self.StudAssigComboBox.currentText()
            if current_text == "Assignments":
                for assign in self._assignment_service.get_assignments:
                    if i == row:
                        assignment_id = assign.entity_id
                    i += 1
            ordered_list = self._grade_service.order_students_by_average_grade_of_assignment(assignment_id)
            average_grade = self._grade_service.get_average_grade_of_assignment(assignment_id)
            average_grade_text = f'the average grade of {assignment_id} is {average_grade}'
            display_data_list.append(average_grade_text)
            for student in ordered_list:
                display_data_list.append(student)
            self.sub_window = SubWindow("Students ordered by average grade of an Assignment",display_data_list)
        elif row == 2:
            display_data_list = self._grade_service.students_late_in_handling_assignments()
            self.sub_window = SubWindow("Students late in handling Assignments",display_data_list)
        elif row == 3:
            display_data_list = self._grade_service.sort_students_by_average_grades()
            self.sub_window = SubWindow("best Students",display_data_list)
        self.sub_window.show()

    def give_grade(self):
        stud_id = self._student_service.get_students[0].entity_id
        row = int(self.dataList.currentRow())
        i = 0
        current_text = self.StudAssigComboBox.currentText()
        if current_text == "Students":
            for stud in self._student_service.get_students:
                if i == row:
                    stud_id = stud.entity_id
                i += 1
        ungraded_assignments = []
        for assigment_id in self._grade_service.get_list_of_ungraded_assignments_for_student(stud_id):
            ungraded_assignments.append(assigment_id)
        self.sub_window = SubWindowGrades(stud_id,ungraded_assignments,self._grade_service)
        self.sub_window.show()

    def give_assignment(self):
        assignment_id = self._assignment_service.get_assignments[0].entity_id
        row = int(self.dataList.currentRow())
        i = 0
        current_text = self.StudAssigComboBox.currentText()
        if current_text == "Assignments":
            for assign in self._assignment_service.get_assignments:
                if i == row:
                    assignment_id = assign.entity_id
                i += 1
        self.sub_window = SubWindowAssignments(assignment_id, self._student_service, self._grade_service)
        self.sub_window.show()

    def gui_undo(self):
        self._undo_redo_service.undo()
        self.refresh_data_list()

    def gui_redo(self):
        self._undo_redo_service.redo()
        self.refresh_data_list()

    def connect_signals_and_slots(self):
        self.StudAssigComboBox.activated.connect(lambda: self.refresh_data_list())
        self.addButton.clicked.connect(lambda: self.add_data_list())
        self.removeButton.clicked.connect(lambda: self.remove_data_list())
        self.updateButton.clicked.connect(lambda: self.update_data_list())
        self.displayButton.clicked.connect(lambda: self.display_data())
        self.gradeButton.clicked.connect(lambda: self.give_grade())
        self.assignmentButton.clicked.connect(lambda: self.give_assignment())
        self.undoButton.clicked.connect(lambda: self.gui_undo())
        self.redoButton.clicked.connect(lambda: self.gui_redo())
        self.dataList.itemClicked.connect(lambda: self.update_text_lines())


class SubWindow(QWidget):
    def __init__(self,title,data_list):
        super(SubWindow, self).__init__()
        self._title = title
        self._data_list = data_list

        self.resize(400, 330)
        self.layout = QVBoxLayout()

        # Label
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 400, 30)
        self.label.setText(self._title)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet('font-size:25px')

        self.data_list_widget = QListWidget(self)
        self.data_list_widget.setGeometry(0, 0, 400, 300)

        self.data_list_widget.clear()
        for data in self._data_list:
            self.data_list_widget.addItem(str(data))

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.data_list_widget)

        self.setLayout(self.layout)

class SubWindowGrades(QWidget):
    def __init__(self, stud_id, ungraded_assignments, grade_service):
        super(SubWindowGrades, self).__init__()
        self._stud_id = stud_id
        self._ungraded_assignments = ungraded_assignments
        self._grade_service = grade_service

        self.resize(400, 330)
        self.layout = QVBoxLayout()

        # Label
        self.assignments_label = QLabel(self)
        self.assignments_label.setGeometry(0, 0, 400, 30)
        self.assignments_label.setText("choose assignment:")
        self.assignments_label.setAlignment(Qt.AlignLeft)
        self.assignments_label.setStyleSheet('font-size:15px')

        self.data_list_widget = QListWidget(self)
        self.data_list_widget.setGeometry(0, 0, 400, 210)

        self.data_list_widget.clear()
        for data in self._ungraded_assignments:
            self.data_list_widget.addItem(str(data))
        self.data_list_widget.setCurrentRow(0)

        self.grade_label = QLabel(self)
        self.grade_label.setGeometry(0, 0, 400, 30)
        self.grade_label.setText("give grade:")
        self.grade_label.setAlignment(Qt.AlignLeft)
        self.grade_label.setStyleSheet('font-size:15px')

        self.grade_line_edit = QLineEdit(self)
        self.grade_line_edit.setGeometry(0, 0, 400, 30)

        self.grade_button = QPushButton(self)
        self.grade_button.setGeometry(0, 0, 400, 30)
        self.grade_button.setText("Give Grade")

        self.layout.addWidget(self.assignments_label)
        self.layout.addWidget(self.data_list_widget)
        self.layout.addWidget(self.grade_label)
        self.layout.addWidget(self.grade_line_edit)
        self.layout.addWidget(self.grade_button)

        self.grade_button.clicked.connect(lambda: self.give_grade())

        self.setLayout(self.layout)

    def give_grade(self):
        row = int(self.data_list_widget.currentRow())
        i = 0
        for assign in self._ungraded_assignments:
            if i == row:
                assignment_id = assign
            i += 1
        grade = int(self.grade_line_edit.text())
        self._grade_service.give_grade_to_student_assignment(self._stud_id, assignment_id, grade)
        self.close()

class SubWindowAssignments(QWidget):
    def __init__(self, assignment_id, student_service, grade_service):
        super(SubWindowAssignments, self).__init__()
        self._assignment_id = assignment_id
        self._student_service = student_service
        self._grade_service = grade_service

        self.resize(400, 330)
        self.layout = QVBoxLayout()

        self.comboBox = QComboBox(self)
        self.comboBox.setGeometry(0,0,400,30)
        self.comboBox.addItem("choose group or student")
        self.comboBox.addItem("Groups")
        self.comboBox.addItem("Students")

        self.data_list_widget = QListWidget(self)
        self.data_list_widget.setGeometry(0, 0, 400, 240)

        self.data_list_widget.clear()

        self.assign_button = QPushButton(self)
        self.assign_button.setGeometry(0, 0, 400, 30)
        self.assign_button.setText("Give Assignment")

        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.data_list_widget)
        self.layout.addWidget(self.assign_button)

        self.comboBox.activated.connect(lambda: self.refresh_data_list())
        self.assign_button.clicked.connect(lambda: self.give_assignment())

        self.setLayout(self.layout)

    def give_assignment(self):
        groups = []
        for stud in self._student_service.get_students:
            if stud.group not in groups:
                groups.append(stud.group)
        row = int(self.data_list_widget.currentRow())
        i = 0
        current_text = self.comboBox.currentText()
        if current_text == "Groups":
            for group in groups:
                if i == row:
                    self._grade_service.give_assignment_to_group_of_students(group, self._assignment_id)
                i += 1
        elif current_text == "Students":
            for stud in self._student_service.get_students:
                if i == row:
                    self._grade_service.give_assignment_to_student(stud.entity_id, self._assignment_id)
                i += 1
        self.refresh_data_list()
        self.close()

    def refresh_data_list(self):
        current_text = self.comboBox.currentText()
        if current_text == "Groups":
            self.data_list_widget.clear()
            groups = []
            for stud in self._student_service.get_students:
                if stud.group not in groups:
                    groups.append(stud.group)
            for group in groups:
                self.data_list_widget.addItem(str(group))

        elif current_text == "Students":
            self.data_list_widget.clear()
            for stud in self._student_service.get_students:
                self.data_list_widget.addItem(str(stud))

        else:
            self.data_list_widget.clear()


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

main()
