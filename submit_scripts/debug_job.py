"""
debug_job.py
Sends a submission job to opencue for debug
"""

import os
import sys
import getpass
import datetime
from modules.debug import DebugLayer
from outline import Outline, cuerun

# Create an outline for the job
job_name = "debug_job"
shot_name = "debug_shot"
show_name = "testing"
user = getpass.getuser()

outline = Outline(job_name, shot=shot_name, show=show_name, user=user)

# Create the debug Layer
layer_name = "debug_layer"
chunk_size = 1
threads = 1.0
threadable = False
frame_range = "1"

debug_layer = DebugLayer(layer_name,
                         input="input_path",
                         output="output_path",
                         chunk=chunk_size,
                         threads=threads,
                         range=frame_range,
                         threadable=threadable,
                         crf=25)

outline.add_layer(debug_layer)

# Submit job
cuerun.launch(outline, use_pycuerun=False)
