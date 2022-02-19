from unittest import TestCase

from domain.entitywithid import EntityWithId


class Student(EntityWithId):
    """
    The class which represents a student
    """

    def __init__(self, student_id, name, group):
        """
        Constructor which creates a student
        :param student_id: uniquely student id (string type)
        :param name: the name of a student (string type)
        :param group: the group where the student belongs (int type)
        """
        super().__init__(student_id)
        self._name = name
        self._group = group

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, new_group):
        self._group = new_group

    def __str__(self):
        return '( ' + self._entity_id + ', ' + self._name + ', ' + str(self._group) + ' )'


