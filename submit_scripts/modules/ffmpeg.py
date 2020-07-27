"""
ffmpeg.py
ffmpeg module for opencue/pyoutline
"""

from outline.layer import Layer, Frame

__all__ = ["MakeMov",
           "CheckMov"]

FFMPEG_CMD = ("ffmpeg -n -i {input} -c:v libx264 -pix_fmt yuv420p "
              "-preset faster -crf {crf} -c:a aac "
              "-movflags +faststart {output}")

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

        command = FFMPEG_CMD.format(input=input_path,
                                    output=output_path,
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

        tmp = self.get_temp_dir()
        self.set_arg("concat_cfg",
                     os.path.join(tmp, self.name + "_concat.txt"))

        with open(self.get_arg("concat_cfg")) as fd:
            inputs_sorted = sorted(self.get_inputs().items())
            for _, path in inputs_sorted:
                fd.write(f"file {path}\n")

        command = CONCAT_CMD.format(concat_cfg=self.get_arg("concat_cfg"),
                                    output=output_path).split()
        self.set_arg("command", command)

    def _execute(self, frame_set):
        """
        Execute the ffmpeg command (the frame set is not necessary,
            since we execute over the whole mov)
        """
        self.system(self.get_arg("command"))
