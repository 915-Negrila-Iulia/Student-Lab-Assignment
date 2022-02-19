from validator.validators import UndoRedoException


class UndoRedoService:
    def __init__(self):
        """
        Create history of operations and an index for the current operation
        """
        self._history_operations = []
        self._index = -1


    def add_operation(self, operation):
        """
        Adds to the history list of operations a new operation
        :param operation: the operation which is added to the history list
        :return: -
        """
        self._history_operations = self._history_operations[:]
        self._history_operations.append(operation)
        self._index += 1

    def undo(self):
        """
        Gets the operation (from the history list of operations) which has to be called in order to undo another
        operation which was previously performed by the user
        Decrease the index for the history list
        :return: -
        Raise UndoRedoException if there are no more undos
        """
        if self._index == -1:
            raise UndoRedoException('No more undos!')

        operation = self._history_operations[self._index]
        operation.undo()
        self._index -= 1

    def redo(self):
        """
        Increase the index for the history list
        Gets the operation (from the history list of operations) which has to be called in order to redo another
        operation which was previously performed by the user
        :return: -
        Raise UndoRedoException if there are no more redos
        """
        if self._index == len(self._history_operations) - 1:
            raise UndoRedoException('No more redos!')

        self._index += 1
        operation = self._history_operations[self._index]
        operation.redo()


class Operation:
    def __init__(self, undo_function, redo_function):
        """
        Constructor for an operation
        :param undo_function: function which will undo an operation performed by the user
        :param redo_function: function which will redo an operation performed by the user
        """
        self._undo_function = undo_function
        self._redo_function = redo_function

    def undo(self):
        self._undo_function()

    def redo(self):
        self._redo_function()


class FunctionCall:
    def __init__(self, name, *parameters):
        """
        Constructor for a function
        :param name: name of the function
        :param parameters: parameters of the function
        """
        self._name = name
        self._parameters = parameters

    def call(self):
        return self._name(*self._parameters)

    def __call__(self):
        return self.call()


class CascadedOperation:
    def __init__(self, *operations):
        """
        Constructor for a cascaded operation
        :param operations: operations which form the cascaded operation
        """
        self._operations = operations

    def undo(self):
        for operation in self._operations:
            operation.undo()

    def redo(self):
        for operation in self._operations:
            operation.redo()
