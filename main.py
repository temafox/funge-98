"""The launcher of the Funge interpreter."""

from funge_impl.funge_interpreter import FungeInterpreter

if __name__ == "__main__":
    PROGRAM = "zk  ;@@@@; ;@;  rz@z"

    interpreter = FungeInterpreter(PROGRAM)
    interpreter.run(log=True)
    interpreter.log_after_termination()
