class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError("pop from empty stack")

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        raise IndexError("peek from empty stack")

    def size(self):
        return len(self.items)

def is_balanced(brackets):
    stack = Stack()
    pairs = {')': '(', '}': '{', ']': '['}

    for bracket in brackets:
        if bracket in pairs.values():  # Если это открывающая скобка
            stack.push(bracket)
        elif bracket in pairs.keys():  # Если это закрывающая скобка
            if stack.is_empty() or stack.pop() != pairs[bracket]:
                return "Несбалансированно"

    return "Сбалансированно" if stack.is_empty() else "Несбалансированно"

# Примеры использования
if __name__ == "__main__":
    examples = [
        "(((([{}]))))",
        "[([])((([[[]]])))]{()}",
        "{{[()]}}",
        "}{",
        "{{[(])]}}",
        "[[{())}]"
    ]

    for example in examples:
        print(f"{example}: {is_balanced(example)}")
