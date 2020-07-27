"""
debug.py
Layer module for opencue that only prints info
"""

from outline.layer import Layer, Frame
import logging

__all__ = ["DebugLayer"]

logger = logging.getLogger("outline.layer")


class DebugLayer(Layer):
    """
    Provides a method to print various debug info using opencue
    """
    def __init__(self, name, **args):
        Layer.__init__(self, name, **args)
        command = ["echo", "'"]
        for arg_n, arg_v in self.get_args().items():
            command.append(f"DebugLayer - Argument {arg_n} set to {arg_v}\n")
        command.append("'")
        self.set_arg("command", command)

    def _execute(self, frame_set):
        self.system(self.get_arg("command"))
