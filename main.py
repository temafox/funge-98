from typing import Callable, Any


class InstructionPointer:
    def __init__(self, delta=1, position=0):
        self.delta = delta
        self.position = position
        self.running = True


class StackOfStacks:
    def __init__(self):
        self.sos = []

    def pop(self, stack_index):
        try:
            return self.sos[stack_index].pop()
        except IndexError:
            return 0

    def push(self, stack_index, value):
        try:
            self.sos[stack_index].append(value)
        except IndexError:
            self.sos.insert(0, [value])


class ProgramSpace:
    def __init__(self, text):
        self.text = text
        self.time = 0
        self.ip = InstructionPointer()

    def make_step(self, ip):
        if not ip.running:
            return
        ip.position += ip.delta
        if ip.position < 0 or ip.position >= len(self.text):
            ip.position -= (len(self.text) // abs(ip.delta)) * ip.delta

    def execute_instruction(self, ip, log):
        if log:
            print(self.text)
            print("".join(['^' if i == self.ip.position else ' ' for i in range(len(self.text))]))
        instruction = get_instruction(self.text[ip.position])
        self.time += instruction(ip)

    def run(self, log):
        self.execute_instruction(self.ip, log)
        while self.ip.running:
            self.make_step(self.ip)
            self.execute_instruction(self.ip, log)


def get_instruction(character):
    if character == '@' or character == 'q':
        def kill_ip(ip):
            ip.delta = 0
            ip.running = False
            return 1
        return kill_ip

    if character == '#':
        def trampoline(ip):
            ip.position += 1 if ip.delta > 0 else -1
            return 1
        return trampoline

    if character == '<':
        def west_unity(ip):
            ip.delta = -1
            return 1
        return west_unity

    if character == '>':
        def east_unity(ip):
            ip.delta = 1
            return 1
        return east_unity

    def nop(ip):
        return 0
    return nop


if __name__ == '__main__':
    program = '#<<@<'
    interpreter = ProgramSpace(program)

    interpreter.run(log=True)
    print(interpreter.time)

