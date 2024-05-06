"""The instruction pointer."""

from funge_impl.program_space import ProgramSpace
from funge_impl.stack_stack import StackStack


class InstructionPointer:
    """The instruction pointer (IP)."""

    def __init__(self, program_space: ProgramSpace):
        self.position = [0]
        self.delta = [1]
        self.program_space = program_space
        self.ss = StackStack()

    def make_step(self, times: int = 1):
        for i in range(len(self.position)):
            self.position[i] += self.delta[i] * times
        if self.position[0] < 0 or self.position[0] >= len(self.program_space.text):
            self.position[0] -= (len(self.program_space.text) // abs(self.delta[0])) * self.delta[0]

    def current_character(self):
        return self.program_space.text[self.position[0]]
