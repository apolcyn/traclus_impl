'''
Created on Jan 2, 2016

@author: Alex
'''
from compiler.ast import Node


class LinkedList:
    def __init__(self):
        self.head = LinkedListNode(None)
        self.head.next = self.head
        self.head.prev = self.head
        self.size = 0
        
    def __iter__(self):
        return LinkedListIter(self)
    
    def __len__(self):
        return self.size
    
    def __getitem__(self, index):
        if index >= self.size or index < 0:
            raise IndexError
        
        cur = self.head.next
        count = 0
        while count < index:
            cur = cur.next
            count += 1
        return cur.item
        
    def add_last(self, item):
        temp = LinkedListNode(item)
        self.add_last_node(temp)
        
    def add_first(self, item):
        temp = LinkedListNode(item)
        self.add_first_node(temp)
        
    def get_first(self):
        if self.empty():
            raise Exception("can't get item from empty list")
        return self.head.next.item
    
    def get_last(self):
        if self.empty():
            raise Exception("can't get item from empty list")
        return self.head.prev.item
    
    def empty(self):
        return self.head == self.head.next
        
    def add_last_node(self, new_node):
        new_node.next = self.head
        new_node.prev = self.head.prev
        self.head.prev.next = new_node
        self.head.prev = new_node
        self.size += 1
        
    def add_first_node(self, new_node):
        new_node.next = self.head.next
        new_node.prev = self.head
        self.head.next.prev = new_node
        self.head.next = new_node
        self.size += 1
        
    def remove_node(self, new_node):
        if self.size == 0:
            raise Exception("trying to remove a node from empty list")
        new_node.next.prev = new_node.prev
        new_node.prev.next = new_node.next
        self.size -= 1
           
class LinkedListNode:
    def __init__(self, item):
        self.item = item
        self.next = None
        self.prev = None
        
class LinkedListIter:
    def __init__(self, list):
        self.list = list
        self.pos = list.head.next
        
    def next(self):
        if self.pos == self.list.head:
            raise StopIteration
        else:
            item = self.pos.item
            self.pos = self.pos.next
            return item