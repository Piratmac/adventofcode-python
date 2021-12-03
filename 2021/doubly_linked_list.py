class DoublyLinkedList:
    def __init__(self, is_cycle=False):
        """
        Creates a list

        :param Boolean is_cycle: Whether the list is a cycle (loops around itself)
        """
        self.start_element = None
        self.is_cycle = is_cycle
        self.elements = {}

    def insert(self, ref_element, new_elements, insert_before=False):
        """
        Inserts new elements in the list

        :param Any ref_element: The value of the element where we'll insert data
        :param Any new_elements: A list of new elements to insert, or a single element
        :param Boolean insert_before: If True, will insert before ref_element.
        """
        new_elements_converted = []
        if isinstance(new_elements, (list, tuple, set)):
            for i, element in enumerate(new_elements):
                if not isinstance(element, DoublyLinkedListElement):
                    new_element_converted = DoublyLinkedListElement(element)
                    if i != 0:
                        new_element_converted.prev_element = new_elements_converted[
                            i - 1
                        ]
                        new_element_converted.prev_element.next_element = (
                            new_element_converted
                        )
                else:
                    new_element_converted = element
                    if i != 0:
                        new_element_converted.prev_element = new_elements_converted[
                            i - 1
                        ]
                        new_element_converted.prev_element.next_element = (
                            new_element_converted
                        )
                new_elements_converted.append(new_element_converted)
                self.elements[new_element_converted.item] = new_element_converted
        else:
            if not isinstance(new_elements, DoublyLinkedListElement):
                new_element_converted = DoublyLinkedListElement(new_elements)
            else:
                new_element_converted = new_elements
            new_elements_converted.append(new_element_converted)
            self.elements[new_element_converted.item] = new_element_converted

        if self.start_element == None:
            self.start_element = new_elements_converted[0]
            for pos, element in enumerate(new_elements_converted):
                element.prev_element = new_elements_converted[pos - 1]
                element.next_element = new_elements_converted[pos + 1]

            if not self.is_cycle:
                new_elements_converted[0].prev_element = None
                new_elements_converted[-1].next_element = None
        else:
            if isinstance(ref_element, DoublyLinkedListElement):
                cursor = ref_element
            else:
                cursor = self.find(ref_element)

            if insert_before:
                new_elements_converted[0].prev_element = cursor.prev_element
                new_elements_converted[-1].next_element = cursor

                if cursor.prev_element is not None:
                    cursor.prev_element.next_element = new_elements_converted[0]
                cursor.prev_element = new_elements_converted[-1]
                if self.start_element == cursor:
                    self.start_element = new_elements_converted[0]
            else:
                new_elements_converted[0].prev_element = cursor
                new_elements_converted[-1].next_element = cursor.next_element
                if cursor.next_element is not None:
                    cursor.next_element.prev_element = new_elements_converted[-1]
                cursor.next_element = new_elements_converted[0]

    def append(self, new_element):
        """
        Appends an element in the list

        :param Any new_element: The new element to insert
        :param Boolean insert_before: If True, will insert before ref_element.
        """
        if not isinstance(new_element, DoublyLinkedListElement):
            new_element = DoublyLinkedListElement(new_element)

        self.elements[new_element.item] = new_element

        if self.start_element is None:
            self.start_element = new_element
            if self.is_cycle:
                new_element.next_element = new_element
                new_element.prev_element = new_element
        else:
            if self.is_cycle:
                cursor = self.start_element.prev_element
            else:
                cursor = self.start_element
                while cursor.next_element is not None:
                    if self.is_cycle and cursor.next_element == self.start_element:
                        break
                    cursor = cursor.next_element

            new_element.prev_element = cursor
            new_element.next_element = cursor.next_element
            if cursor.next_element is not None:
                cursor.next_element.prev_element = new_element
            cursor.next_element = new_element

    def traverse(self, start, end=None):
        """
        Gets items based on their values

        :param Any start: The start element
        :param Any stop: The end element
        """
        output = []
        if self.start_element is None:
            return []

        if not isinstance(start, DoublyLinkedListElement):
            start = self.find(start)
        cursor = start

        if not isinstance(end, DoublyLinkedListElement):
            end = self.find(end)

        while cursor is not None:
            if cursor == end:
                break

            output.append(cursor)

            cursor = cursor.next_element

            if self.is_cycle and cursor == start:
                break

        return output

    def delete_by_value(self, to_delete):
        """
        Deletes a given element from the list

        :param Any to_delete: The element to delete
        """
        output = []
        if self.start_element is None:
            return

        cursor = to_delete
        cursor.prev_element.next_element = cursor.next_element
        cursor.next_element.prev_element = cursor.prev_element

    def delete_by_position(self, to_delete):
        """
        Deletes a given element from the list

        :param Any to_delete: The element to delete
        """
        output = []
        if self.start_element is None:
            return

        if not isinstance(to_delete, int):
            raise TypeError("Position must be an integer")

        cursor = self.start_element
        i = -1
        while cursor is not None and i < to_delete:
            i += 1
            if i == to_delete:
                if cursor.prev_element:
                    cursor.prev_element.next_element = cursor.next_element
                if cursor.next_element:
                    cursor.next_element.prev_element = cursor.prev_element

                if self.start_element == cursor:
                    self.start_element = cursor.next_element

                del cursor
                return True

        raise ValueError("Element not in list")

    def find(self, needle):
        """
        Finds a given item based on its value

        :param Any needle: The element to search
        """
        if isinstance(needle, DoublyLinkedListElement):
            return needle
        else:
            if needle in self.elements:
                return self.elements[needle]
            else:
                return False


class DoublyLinkedListElement:
    def __init__(self, data, prev_element=None, next_element=None):
        self.item = data
        self.prev_element = prev_element
        self.next_element = next_element

    def __repr__(self):
        output = [self.item]
        if self.prev_element is not None:
            output.append(self.prev_element.item)
        else:
            output.append(None)
        if self.next_element is not None:
            output.append(self.next_element.item)
        else:
            output.append(None)
        return str(tuple(output))
