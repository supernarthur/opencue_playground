"""
ffmpeg.py
ffmpeg module for opencue/pyoutline
"""

from outline.layer import Layer, Frame

__all__ = ["MakeMov",
           "CheckMov"]

FFMPEG_CMD = ("ffmpeg -i {input} -c:v libx264 -pix_fmt yuv420p "
              "-preset faster -crf {crf} -c:a aac "
              "-movflags +faststart {output}")

VMAF_CMD = ("ffmpeg -i {input} -i {ref} -lavfi libvmaf "
            "-f null -")


class MakeMov(Layer):
    """
    Provides a method to execute an ffmpeg command using opencue framework
    """
    def __init__(self, name, **args):
        Layer.__init__(self, name, **args)

        self.require_arg("input")
        self.require_arg("output")
        self.require_arg("crf")
        command = FFMPEG_CMD.format(input=self.get_arg("input"),
                                    output=self.get_arg("output"),
                                    crf=self.get_arg("crf")).split(" ")
        self.set_arg("command", command)

    def _execute(self, frame_set):
        """
        Execute the ffmpeg command (the frame set is not necessary,
            since we execute over the whole mov)
        """
        self.system(self.get_arg("command"))


class CheckMov(Layer):
    """
    Provides a method to execute a vmaf check of a file
    against a reference video file using opencue framework
    """
    def __init__(self, name, **args):
        Layer.__init__(self, name, **args)

        self.require_arg("input")
        self.require_arg("ref")
        command = VMAF_CMD.format(input=self.get_arg("input"),
                                  ref=self.get_arg("ref")).split(" ")
        self.set_arg("command", command)

    def _execute(self, frame_set):
        """
        Execute the ffmpeg command (the frame set is not necessary,
            since we execute over the whole mov)
        """
        self.system(self.get_arg("command"))
