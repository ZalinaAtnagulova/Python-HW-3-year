class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def empty(self):
        if self.head:
            return False
        return True

    def printList(self):
        node = self.head
        while node:
            print(node.data, end="->")
            node = node.next
        print()

    def push(self, data):
        node = Node(data, next=self.head)
        self.head = node

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = new_node

    def insert(self, value, index):
        node = self.head
        inserted = Node(value)
        dex = 0
        while node:
            dex += 1
            if dex == (index-1):
                old_value = node.next.data
                old_link = node.next.next
                node.next = inserted
                old_new = Node(old_value, old_link)
                inserted.next = old_new
            node = node.next

    def delete(self, value):
        node = self.head
        while node.next:
            if self.back() == value:
                self.pop_back()
            if self.head.data == value:
                self.pop_head()
            if node.data == value:
                node.data = node.next.data
                node.next = node.next.next
            if node.next.data == value:
                node.next = node.next.next
            node = node.next
    
    def size(self):
        node = self.head
        idex = 0
        while node:
            idex += 1
            node = node.next
        return(idex)

    def pop_back(self):
        node = self.head
        while node:
            if node.next.next is None:
                deleted = node.next.data
                node.next = None
            node = node.next
        return deleted

    def pop_head(self):
        node = self.head
        if node.next is not None:
            deleted = node.data
            self.head = node.next
        return deleted

    def back(self):
        node = self.head
        while node:
            if node.next is None:
                return(node.data)
            node = node.next

    def value_n_from_end(self, n):
        node = self.head
        dex = 0
        while node:
            dex += 1
            if dex == (self.size() - n + 1):
                return node
            node = node.next


l = LinkedList()
for i in [6,6,8,2,3,4,5,4,5,6,6,1,1,54,3,6,6]:
    l.append(i)
l.printList()
l.push(6)
l.insert(19, 6)
l.printList()
print(l.size())
l.delete(6)
l.printList()
print(l.value_n_from_end(2).data)
