class MyQueue:
    def __init__(self):
        self.arr = []
        self.que = []
        
    def enqueue(self, fun1, fun2):
        for one in self.arr:
            fun1.push(one)
        for a in range(len(fun1.inp)):
            fun2.push(fun1.peek())
            fun1.pop()
            a += 1
        self.que = fun2.inp
        
    def dequeue(self, fun2):
         if not fun2.isEmpty():
             return fun2.pop()
             
    def peek(self, fun2):
         if not fun2.isEmpty():
             return fun2.peek()
              
    def isEmpty(self, fun2):
          if len(fun2.inp) == 0:
              return True
          return False

class Stack:
      def __init__(self): 
          self.inp = []

      def push(self, elem):
          self.inp.append(elem)

      def peek(self):
          if not self.isEmpty():
              return self.inp[-1]
        
      def pop(self):
          if not self.isEmpty():
              last = self.inp[-1]
              self.inp.remove(self.inp[-1])
              return last
    
      def isEmpty(self):
          if len(self.inp) != 0:
                return False
          return True

array = []
st1 = Stack()
st2 = Stack()
queue = MyQueue()
for a in range(0, 10):
    array.append(a)
queue.arr = array
queue.enqueue(st1, st2)
print(queue.que)
print(queue.dequeue(st2))
print(queue.que)
print(queue.peek(st2))
print(queue.isEmpty(st2))
