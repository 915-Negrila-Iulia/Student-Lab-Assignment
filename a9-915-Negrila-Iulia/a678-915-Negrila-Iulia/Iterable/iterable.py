import unittest


class Iterable:
    """

    """

    def __init__(self):
        self._elements = []
        self._index = 0

    def __getitem__(self, index):
        return self._elements[index]

    def __setitem__(self, index, new_element):
        self._elements[index] = new_element

    def __delitem__(self, index):
        del self._elements[index]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index == len(self._elements):
            raise StopIteration()
        self._index += 1
        return self._elements[self._index - 1]

    def __len__(self):
        return len(self._elements)

    def append(self, new_element):
        self._elements.append(new_element)

    def remove(self, element):
        self._elements.remove(element)

    def shell_sort(self, comparison_function):
        """
        Sorting the elements of a list by a given condition
        :param comparison_function: the condition of sorting
        :return: -
        """
        # Rearrange elements at each length/2, length/4, length/8, ... intervals
        interval = int(len(self._elements) / 2)
        while interval > 0:

            for first_index in range(interval, len(self._elements)):
                element_to_compare = self._elements[first_index]
                second_index = first_index

                while second_index >= interval and not comparison_function(self._elements[second_index - interval],
                                                                           element_to_compare):
                    self._elements[second_index] = self._elements[second_index - interval]
                    second_index -= interval
                self._elements[second_index] = element_to_compare

            interval = int(interval / 2)

    def filter(self, comparison_function):
        """
        Filters a list by a given condition
        :param comparison_function:
        :return:
        """
        index = 0
        while index < len(self._elements):
            if not comparison_function(self._elements[index]):
                del self._elements[index]
            else:
                index += 1

class IterableTest(unittest.TestCase):
    def test_iterable(self):
        test_list = Iterable()
        first_number = 0
        second_number = 1
        third_number = 2
        new_list = test_list.__iter__()
        self.assertEqual(new_list, test_list)
        self.assertRaises(StopIteration, test_list.__next__)
        for index in range(0, 3):
            test_list.append(index)
        self.assertEqual(test_list.__next__(), test_list[first_number])
        for index in range(0, 3):
            self.assertEqual(test_list[index], index)
        self.assertEqual(test_list[first_number], 0)
        self.assertEqual(test_list[second_number], 1)
        self.assertEqual(test_list[third_number], 2)
        self.assertEqual(len(test_list), 3)
        del test_list[first_number]
        self.assertEqual(len(test_list), 2)
        test_list[first_number] = 4
        self.assertEqual(test_list[first_number], 4)
        test_list.remove(test_list[second_number])
        self.assertEqual(len(test_list), 1)

        test_list1 = Iterable()
        test_list1.append(2)
        test_list1.append(1)
        test_list1.append(4)
        test_list1.append(0)
        test_list1.append(3)
        test_list1.shell_sort(lambda first_element_to_compare,
                                     second_element_to_compare: first_element_to_compare < second_element_to_compare)
        for index in range(0,5):
            self.assertEqual(test_list1[index], index)

        test_list1.shell_sort(lambda first_element_to_compare,
                                      second_element_to_compare: first_element_to_compare > second_element_to_compare)
        for index in range(0,5):
             self.assertEqual(test_list1[index], 4-index)

        test_list2 = Iterable()
        test_list2.append(2)
        test_list2.append(1)
        test_list2.append(4)
        test_list2.append(0)
        test_list2.append(3)
        test_list2.filter(lambda x: x > 3)
        self.assertEqual(len(test_list2),1)
        self.assertEqual(test_list1[first_number],4)
