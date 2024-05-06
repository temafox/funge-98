"""Implementation of Funge-98."""

from funge_impl.instruction_pointer import InstructionPointer
from funge_impl.instructions import get_instruction_handler
from funge_impl.program_space import ProgramSpace


class FungeInterpreter:
    """The Funge-98 interpreter."""
    def __init__(self, text: str):
        self.program_space = ProgramSpace(text)
        self.ip = InstructionPointer(self.program_space)
        self.ticks = 0
        self.return_code = 0

    def log_ticks(self):
        print("ticks = {}".format(self.ticks))

    def log_program_state(self):
        print(self.program_space.text)
        print(
            "^".join(
                [" " * self.ip.position[0], " " * (len(self.program_space.text) - self.ip.position[0] - 1)]
            )
        )
        print(self.ip.ss.ss)

    def log_before_execution(self):
        self.log_ticks()
        self.log_program_state()
        print()

    def log_after_termination(self):
        print("Program terminated.")
        self.log_ticks()
        self.log_program_state()
        print("return code = {}".format(self.return_code))

    def execute_instruction(self, ip: InstructionPointer,):
        instruction_handler = get_instruction_handler(self.program_space.text[ip.position[0]])
        result = instruction_handler(ip)
        if ip.delta == 0:
            self.return_code = result
        else:
            self.ticks += result

    def run(self, log: bool):
        if log:
            self.log_before_execution()
        self.execute_instruction(self.ip)
        while self.ip.delta != [0]:
            self.ip.make_step()
            if log:
                self.log_before_execution()
            self.execute_instruction(self.ip)
