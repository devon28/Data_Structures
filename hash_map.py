# Name: Devon Miller
# OSU Email: milldevo@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 7
# Due Date: 12/3/2021
# Description: a hash table with 2 possible hash functions, hash table
#               is represented by a dynamic array with each element in the
#               array a linked list, HashMap class has methods clear, get,
#               put, remove, resize, contains, get_keys, empty_buckets and
#               table_load


# Import pre-written DynamicArray and LinkedList classes
from a7_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        clears the HashMap class by setting self.buckets to a new
        dynamic array populated by linked lists with capacity unchanged
        """
        self.buckets = DynamicArray()
        self.size = 0
        for i in range(self.capacity):         # populate empty array with linked lists
            self.buckets.append(LinkedList())


    def get(self, key: str) -> object:
        """
        returns the value associated with a given key, if the
        key is not in the hash map None is returned
        """
        hash = self.hash_function(key)
        index = hash % self.capacity              # index of key
        i = self.buckets.get_at_index(index)
        node = i.contains(key)
        if node is not None:
            return node.value
        return None


    def put(self, key: str, value: object) -> None:
        """
        adds a key value pair to the hash map, if key is already in
        hash map the value for that key is overwritten, if head of linked
        list at index is not None the input key value pair is the new head
        node
        """
        hash = self.hash_function(key)
        index = hash % self.capacity                 # index to be added
        i = self.buckets.get_at_index(index)
        node = i.contains(key)
        if node is not None:
            node.value = value
            return
        i.insert(key, value)
        self.size += 1


    def remove(self, key: str) -> None:
        """
        node associated with input key removed from linked list and hash map,
        if key is not in hash map this method does nothing
        """
        hash = self.hash_function(key)
        index = hash % self.capacity                     # index for key
        i = self.buckets.get_at_index(index)
        i.remove(key)


    def contains_key(self, key: str) -> bool:
        """
        searches hash map for key, returns true if key is found,
        returns false if key not found
        """
        hash = self.hash_function(key)
        index = hash % self.capacity             # index associated with key
        i = self.buckets.get_at_index(index)
        contains = i.contains(key)
        if contains == None:
            return False
        return True


    def empty_buckets(self) -> int:
        """
        returns the number of empty buckets (linked list at index) in
        hash map
        """
        count = 0
        for i in range(self.capacity):            # iterate through hash map
            node = self.buckets.get_at_index(i)
            if node.length() == 1:
                count += 1
        return count


    def table_load(self) -> float:
        """
        returns the table load, size/capacity
        """
        return self.size / self.capacity


    def resize_table(self, new_capacity: int) -> None:
        """
        resizes hash map, does nothing if new_capacity is less than one,
        updates capacity and copies all elements into resized hash map using
        new index based on new capacity, calls put method to add elements
        """
        if new_capacity < 1:
            return
        new = DynamicArray()
        for i in range(new_capacity):
            new.append(LinkedList())
        array = self.buckets  # copy of current hash map
        self.buckets = new  # hash map now resized array populated by linked lists
        old_capacity = self.capacity  # old capacity saved
        self.capacity = new_capacity
        self.size = 0  # size to update when elements added
        for i in range(old_capacity):
            k = array.get_at_index(i)
            node = k.get_first()
            if node is not None:
                self.put(node.key, node.value)  # linked list head added
                while node.next is not None:
                    self.put(node.next.key, node.next.value)
                    node = node.next

    def get_keys(self) -> DynamicArray:
        """
        returns a dynamic array containing all keys in
        the hash map
        """
        keys = DynamicArray()                      # array to be populated by keys
        for i in range(self.capacity):
            k = self.buckets.get_at_index(i)
            node = k.get_first()
            while node is not None:                # all keys in linked list to be appended to keys array
                keys.append(node.key)              # append key
                node = node.next
        return keys


# BASIC TESTING
if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)


    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())


    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)


    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)


    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))


    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)


    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))


    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)


    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')


    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))


    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))


    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())
