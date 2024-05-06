"""Funge-98 instructions."""

from funge_impl.instruction_pointer import InstructionPointer
from funge_impl.stack_stack import StackStack

import random
from typing import Callable


def pop_vector(ss: StackStack, length: int) -> list[int]:
    return [ss.pop_value(-1) for _ in range(length)][::-1]


def generate_cardinal_deltas(dim: int) -> list[list[int]]:
    return [[e if x == i else 0 for x in range(dim)] for i in range(dim) for e in [-1, 1]]


def skip_to_next_semicolon(ip: InstructionPointer):
    """Make at least one step and then stop at the first semicolon."""
    ip.make_step()
    while ip.current_character() != ";":
        ip.make_step()
        
        
def skip_whitespace(ip: InstructionPointer):
    """Make optional steps and stop at the first non-space character."""
    while ip.current_character() == " ":
        ip.make_step()
        
        
def skip_to_next_meaningful_cell(ip: InstructionPointer):
    """
    Make optional steps and stop at the first non-space character
    that is also not hidden between an opening semicolon and a closing semicolon.
    """
    while ip.current_character() in [" ", ";"]:
        if ip.current_character() == " ":
            skip_whitespace(ip)
        else:
            skip_to_next_semicolon(ip)
            ip.make_step()


def get_instruction_handler(character: str) -> Callable[[InstructionPointer], int]:
    """Return a function that executes the encoded instruction."""
    if character == "@":
        def stop(ip: InstructionPointer):
            ip.delta = [0]
            return 0

        return stop

    elif character == "q":
        def f_quit(ip: InstructionPointer):
            ip.delta = [0]
            return_value = ip.ss.pop_value(-1)
            return return_value

        return f_quit

    elif character == "#":
        def trampoline(ip: InstructionPointer):
            for i in range(len(ip.position)):
                ip.position[i] += ip.delta[i]
            return 1

        return trampoline

    elif character == "<":
        def go_west(ip: InstructionPointer):
            ip.delta = [-1]
            return 1

        return go_west

    elif character == ">":
        def go_east(ip: InstructionPointer):
            ip.delta = [1]
            return 1

        return go_east

    elif character == "r":
        def reverse(ip: InstructionPointer):
            for i in range(len(ip.delta)):
                ip.delta[i] *= -1
            return 1

        return reverse

    elif character == "x":
        def absolute_vector(ip: InstructionPointer):
            new_delta = pop_vector(ip.ss, 1)
            ip.delta = new_delta
            return 1

        return absolute_vector

    elif character == "?":
        def go_away(ip: InstructionPointer):
            new_delta = random.choice(generate_cardinal_deltas(1))
            ip.delta = new_delta
            return 1

        return go_away

    elif character == "z":
        def nop_one_tick(_ip):
            return 1

        return nop_one_tick

    elif character == ";":
        def jump_over(ip: InstructionPointer):
            skip_to_next_semicolon(ip)
            return 0

        return jump_over

    elif character == "j":
        def jump_forward(ip: InstructionPointer):
            times = ip.ss.pop_value(-1)
            ip.make_step(times)
            return 1

        return jump_forward

    elif character == "k":
        def iterate(ip: InstructionPointer):
            times = ip.ss.pop_value(-1)
            ip.make_step()
            skip_to_next_meaningful_cell(ip)
            if times > 0:
                instruction_handler = get_instruction_handler(ip.current_character())
                for i in range(times):
                    instruction_handler(ip)
            return 1

        return iterate

    else:
        # No matching instruction found
        return lambda _ip: 0
