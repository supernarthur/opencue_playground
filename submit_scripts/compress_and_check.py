"""
compress_and_check.py
Sends a submission job to opencue for a simple compression,
then checks it using vmaf library
"""

import os
import sys
import getpass
import datetime
from modules.ffmpeg import MakeMov, CheckMov
from outline import Outline, cuerun

# Create an outline for the job
input_file = sys.argv[1]
crf = int(sys.argv[2])
input_path = os.path.abspath(input_file)
shot_name = os.path.basename(input_path)
job_name = f"comp_and_check_{crf}"
show_name = "testing"
user = getpass.getuser()

outline = Outline(job_name, shot=shot_name, show=show_name, user=user)

# Create the MakeMov Layer
layer_name = "makemov"
chunk_size = 1
threads = 1.0
threadable = False
frame_range = "1"

output_path = os.path.splitext(input_path)[0] + f"_H264_{crf}.mp4"

makemov_layer = MakeMov(layer_name, input=input_path, output=output_path,
                        chunk=chunk_size, threads=threads, range=frame_range,
                        threadable=threadable, crf=crf)

outline.add_layer(makemov_layer)

# Create the CheckMov Layer
layer_name = "checkmov"
checkmov_layer = CheckMov(layer_name, input=output_path, ref=input_path,
                          chunk=chunk_size, threads=threads, range=frame_range,
                          threadable=threadable)
checkmov_layer.depend_all(makemov_layer)
outline.add_layer(checkmov_layer)

# Submit job
cuerun.launch(outline, use_pycuerun=False)
