"""The Funge-98 stack stack."""


class StackStack:
    """
    The int stack stack (i.e. the stack of stacks of ints).
    Enumeration of stacks and of integer values is bottom to top.
    """

    ss: list[list[int]] = []

    def __init__(self):
        self.push_stack()

    def push_stack(self):
        """
        Push an empty stack onto the top of the stack stack.
        """
        self.ss.append([])

    def pop_stack(self):
        """
        Pop the top stack of the stack stack and return it.
        Any IndexError will be rethrown.
        """
        try:
            return self.ss.pop()
        except IndexError:
            raise

    def pop_value(self, stack_index):
        """
        Pop a value off the top of an indicated stack and return that value.
        If there is no value on the indicated stack or no such stack, return 0.
        """
        try:
            return self.ss[stack_index].pop()
        except IndexError:
            return 0

    def push_value(self, stack_index, value):
        """
        Push a value onto the top of an indicated stack.
        Any invalid-access error will be rethrown.
        """
        self.ss[stack_index].append(value)
