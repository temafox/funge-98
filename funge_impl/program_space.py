"""The Funge-Space, or the program space to keep the Funge code."""

import dataclasses


@dataclasses.dataclass
class ProgramSpace:
    text: str
