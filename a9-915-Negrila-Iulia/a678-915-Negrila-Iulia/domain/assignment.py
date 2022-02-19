import datetime

from domain.entitywithid import EntityWithId


class Assignment(EntityWithId):
    """
        The class which represents a student assignment
    """

    def __init__(self, assignment_id, description, deadline):
        """
        Constructor which creates an assignment
        :param assignment_id: uniquely assignment id (string type)
        :param description: details about an assignment (string type)
        :param deadline: the date until an assignment can be done (it includes day-month-year) (datetime type)
        """
        super().__init__(assignment_id)
        self._description = description
        self._deadline = deadline

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        self._description = new_description

    @property
    def deadline(self):
        return self._deadline

    @deadline.setter
    def deadline(self,new_deadline):
        self._deadline = new_deadline

    def __str__(self):
        return '( ' + self.entity_id + ', ' + self._description + ', ' + str(self._deadline) + ' )'



