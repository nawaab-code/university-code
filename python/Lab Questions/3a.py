# Stack:

# Stack of 4 elements
stack = ['a','b','c','d']

# Pushing an element 'e' into the stack
stack.append('e')

print(f"Stack after pushing an 'e':\t{stack}") # Output: ['a','b','c','d','e']

# Popping (removing) the top element ('e')
print(f"Popped element:\t{stack.pop()}")  # Output: 'e'
print(f"Stack after pop:\t{stack}") # Output: ['a','b','c','d']

# Peeking (viewing the top element)
if len(stack) > 0:
    print(f"Top element:\t{stack[len(stack)-1]}")  # Output: 'd'
else:
    print("Stack is empty!")


# Queue:

# Queue of 4 elements
queue = ['a','b','c','d']

# Enqueuing  an element 'e' into the queue
queue.append('e')

print(f"Queue after pushing an 'e':\t{queue}") # Output: ['a','b','c','d','e']

print("Queue after enqueues:", queue)  # Output: [100, 200, 300]

# Dequeue (remove) the front element
print(f"Popped element:\t{queue.pop(0)}")  # Output: 'a'
print(f"Queue after pop:\t{queue}") # Output: ['a','b','c','d']

# Peeking (viewing the front element)
if len(queue) > 0:
    print(f"Front element:\t{queue[0]}")  # Output: 'b'
else:
    print("Queue is empty!")