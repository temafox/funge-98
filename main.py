"""Implementation of Unefunge-98."""

from funge_impl.instruction_pointer import InstructionPointer
from funge_impl.instructions import get_instruction_handler
from funge_impl.stack_stack import StackStack


class ProgramSpace:
    def __init__(self, text):
        self.text = text
        self.ticks = 0
        self.ip = InstructionPointer()
        self.ss = StackStack()
        self.return_code = 0

    def log_ticks(self):
        print("ticks = {}".format(self.ticks))

    def log_program_state(self):
        print(self.text)
        print(
            "^".join(
                [" " * self.ip.position[0], " " * (len(self.text) - self.ip.position[0] - 1)]
            )
        )

    def log_before_execution(self):
        self.log_ticks()
        self.log_program_state()

    def log_after_termination(self):
        print("Program terminated.")
        self.log_ticks()
        self.log_program_state()
        print("return code = {}".format(self.return_code))

    def make_step(self, ip: InstructionPointer):
        for i in range(len(ip.position)):
            ip.position[i] += ip.delta[i]
        if ip.position[0] < 0 or ip.position[0] >= len(self.text):
            ip.position[0] -= (len(self.text) // abs(ip.delta[0])) * ip.delta[0]

    def execute_instruction(self, ip: InstructionPointer, ss: StackStack):
        instruction_handler = get_instruction_handler(self.text[ip.position[0]])
        result = instruction_handler(ip, ss)
        if ip.delta == 0:
            self.return_code = result
        else:
            self.ticks += result

    def run(self, log: bool):
        if log:
            self.log_before_execution()
        self.execute_instruction(self.ip, self.ss)
        while self.ip.delta != [0]:
            self.make_step(self.ip)
            if log:
                self.log_before_execution()
            self.execute_instruction(self.ip, self.ss)


if __name__ == "__main__":
    PROGRAM = "zz?#@r"

    interpreter = ProgramSpace(PROGRAM)
    interpreter.run(log=True)
    interpreter.log_after_termination()
