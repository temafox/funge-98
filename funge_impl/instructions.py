"""Funge-98 instructions."""

from funge_impl.instruction_pointer import InstructionPointer
from funge_impl.stack_stack import StackStack

import random
from typing import Callable


def pop_vector(ss: StackStack, length: int) -> list[int]:
    return [ss.pop_value(-1) for _ in range(length)][::-1]


def generate_cardinal_deltas(dim: int) -> list[list[int]]:
    return [[e if x == i else 0 for x in range(dim)] for i in range(dim) for e in [-1, 1]]


def get_instruction_handler(character: str) -> Callable[[InstructionPointer, StackStack], int]:
    """Return a function that executes the encoded instruction."""
    if character == "@":
        def stop(ip: InstructionPointer, _ss):
            ip.delta = [0]
            return 0

        return stop

    if character == "#":
        def trampoline(ip: InstructionPointer, _ss):
            for i in range(len(ip.position)):
                ip.position[i] += ip.delta[i]
            return 1

        return trampoline

    if character == "<":
        def go_west(ip: InstructionPointer, _ss):
            ip.delta = [-1]
            return 1

        return go_west

    if character == ">":
        def go_east(ip: InstructionPointer, _ss):
            ip.delta = [1]
            return 1

        return go_east

    if character == "r":
        def reverse(ip: InstructionPointer, _ss):
            for i in range(len(ip.delta)):
                ip.delta[i] *= -1
            return 1

        return reverse

    if character == "x":
        def absolute_vector(ip: InstructionPointer, ss: StackStack):
            new_delta = pop_vector(ss, 1)
            ip.delta = new_delta
            return 1

        return absolute_vector

    if character == "?":
        def go_away(ip: InstructionPointer, _ss):
            new_delta = random.choice(generate_cardinal_deltas(1))
            ip.delta = new_delta
            return 1

        return go_away

    if character == "z":
        def nop_one_tick(_ip, _ss):
            return 1

        return nop_one_tick

    # No matching instruction found
    def nop_zero_ticks(_ip, _ss):
        return 0

    return nop_zero_ticks
