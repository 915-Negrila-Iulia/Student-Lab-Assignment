class EntityWithId:
    """
    Objects of this type have an id property used to uniquely identify them
    """

    def __init__(self, entity_id):
        self._entity_id = entity_id

    @property
    def entity_id(self):
        return self._entity_id
