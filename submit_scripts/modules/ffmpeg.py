"""
ffmpeg.py
ffmpeg module for opencue/pyoutline
"""

import os
from outline.layer import Layer, Frame

__all__ = ["MakeMov",
           "CheckMov"]

MOV_CMD = ("ffmpeg -n -i {input} -c:v libx264 -pix_fmt yuv420p "
           "-preset faster -crf {crf} -c:a aac "
           "-movflags +faststart {output}")

SEQTOMOV_CMD = ("ffmpeg -n -f image2 -framerate {framerate} "
                "-start_number #IFRAME# -i {input} "
                "-to $(echo \"scale=4;#FRAME_CHUNK#/{framerate}\"| bc) "
                "-c:v libx264 -pix_fmt yuv420p -preset faster "
                "-crf {crf} -movflags +faststart {output}")

VMAF_CMD = ("ffmpeg -i {input} -i {ref} -lavfi "
            "\"libvmaf=n_subsample=4:pool=perc10\" "
            "-f null -")

CONCAT_CMD = ("ffmpeg -n -f concat -safe 0 -i {concat_cfg} -c copy "
              "-movflags +faststart {output}")


class MakeMov(Layer):
    """
    Provides a method to execute an ffmpeg command using opencue framework
    Requires :
    - 1 input
    - 1 output
    - arg "crf" (H.264 quality)
    """
    def __init__(self, name, **args):
        Layer.__init__(self, name, **args)
        self.require_arg("crf")

    def _setup(self):
        """
        Setup steps before layer execution
        """
        assert len(self.get_inputs()) == 1
        assert len(self.get_outputs()) == 1

        output_path = [path for path in self.get_outputs().values()][0]
        input_path = [path for path in self.get_inputs().values()][0]

        command = MOV_CMD.format(input=input_path,
                                 output=output_path,
                                 crf=self.get_arg("crf")).split(" ")
        self.set_arg("command", command)

    def _execute(self, frame_set):
        """
        Execute the ffmpeg command (the frame set is not necessary,
            since we execute over the whole mov)
        """
        self.system(self.get_arg("command"))


class SeqToMov(Layer):
    """
    Provides a method to create a H.264 file from an image sequence
    using the opencue framework
    Requires :
    - 1 input (has to be compatible with ffmpeg image2 demux,
        e.g. using a %0Nd pattern)
    - 1 output
    - arg "fps"
    - arg "crf" (H.264 quality)
    - arg "crstart_framef" the index of the first frame that
        would replace the %0Nd in the input path
    """
    def _setup(self):
        """
        Setup steps before execution
        """
        self.require_arg("fps")
        self.require_arg("crf")
        self.require_arg("start_frame")

        assert len(self.get_inputs()) == 1
        assert len(self.get_outputs()) == 1

        output_path = [path for path in self.get_outputs().values()][0]
        input_path = [path for path in self.get_inputs().values()][0]

        command = SEQTOMOV_CMD.format(input=input_path, output=output_path,
                                      framerate=self.get_arg("fps"),
                                      crf=self.get_arg("crf"))
        command = command.split()
        self.set_arg("command", command)

    def _execute(self, frame_set):
        """
        Execute the ffmpeg command over the frame set
        """
        self.system(self.get_arg("command"))


class CheckMov(Layer):
    """
    Provides a method to execute a vmaf check of a file
    against a reference video file using opencue framework
    Requires :
    - 1 input named "main"
    - 1 input named "ref"
    """

    # __init__ is unchanged

    def _setup(self):
        """
        Setup steps before layer execution
        """
        main_input = self.get_input("main")
        ref_input = self.get_input("ref")

        command = VMAF_CMD.format(input=main_input,
                                  ref=ref_input).split(" ")
        self.set_arg("command", command)

    def _execute(self, frame_set):
        """
        Execute the ffmpeg command (the frame set is not necessary,
            since we execute over the whole mov)
        """
        self.system(self.get_arg("command"))


class ConcatMov(Layer):
    """
    Provides a method to concatenate similarly encoded movie files
    using opencue framework
    """

    # __init__ is unchanged

    def _setup(self):
        """
        Setup steps before layer execution
        Will generate a temporary text file in the form of
            file {file_path}
        for each input.
        It will be used by ffmpeg concat filter during execution
        Order is determined by key in Layer.get_inputs() dict
        """
        assert len(self.get_inputs()) > 0
        assert len(self.get_outputs()) == 1

        output_path = [path for path in self.get_outputs().values()][0]
        input_dir = [os.path.split(str(path))[0]
                     for path in self.get_outputs().values()][0]
        concat_cfg = os.path.join(input_dir, self.get_name() + "_concat.txt")
        with open(concat_cfg, "w") as fd:
            for path in self.get_inputs().values():
                clean_path = str(path).split("'")[1]
                fd.write(f"file {clean_path}\n")

        command = CONCAT_CMD.format(concat_cfg=concat_cfg,
                                    output=output_path).split()
        self.set_arg("command", command)

    def _execute(self, frame_set):
        """
        Execute the ffmpeg command (the frame set is not necessary,
            since we execute over the whole mov)
        """
        self.system(self.get_arg("command"))

    def _after_execute(self):
        """
        Cleanup of the config file
        """
        # os.remove(self.get_arg("concat_cfg"))
