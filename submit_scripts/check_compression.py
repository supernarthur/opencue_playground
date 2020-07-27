"""
check_compression.py
Sends a submission job to opencue for a vmaf check of a file
against a reference file
"""

import os
import sys
import getpass
import datetime
from modules.ffmpeg import CheckMov
from outline import Outline, cuerun

# Create an outline for the job
input_file = sys.argv[1]
input_path = os.path.abspath(input_file)
shot_name = os.path.basename(input_path)
ref_file = sys.argv[2]
ref_path = os.path.abspath(ref_file)
job_name = "check_compress"
show_name = "testing"
user = getpass.getuser()

outline = Outline(job_name, shot=shot_name, show=show_name, user=user)

# Create the CheckMov Layer
layer_name = "checkmov"
chunk_size = 1
threads = 1.0
threadable = False
frame_range = "1"

checkmov_layer = CheckMov(layer_name, chunk=chunk_size, threads=threads,
                          range=frame_range, threadable=threadable)
checkmov_layer.add_input("main", input_path)
checkmov_layer.add_input("ref", ref_path)

outline.add_layer(checkmov_layer)

# Submit job
cuerun.launch(outline, use_pycuerun=False)
