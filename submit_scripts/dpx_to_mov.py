"""
dpx_to_mov.py
Sends a submission job to opencue for a compression using
an image sequence as the input
"""

import os
import re
import sys
import getpass
import datetime
import argparse
from modules.ffmpeg import SeqToMov
from outline import Outline, cuerun


def get_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description="Submits a job to OpenCue")
    parser.add_argument("input_path", type=str,
                        help=("path to the input image sequence "
                              "(first frame)"))
    parser.add_argument("-f", "--fps", type=int, metavar="fps", default=25,
                        help="framerate of the desired output")
    parser.add_argument("-q", "--crf", type=int, metavar="crf", default=25,
                        help="quality of the output (see ffmpeg/x264 crf)")
    parser.add_argument("-c", "--chunk", type=int, metavar="chunk",
                        default=600,
                        help="size in frames of the render chunks")
    parser.add_argument("-o", "--output", type=str, metavar="output_path",
                        default="", help="The path to the output file")
    return parser.parse_args()


def translate_imgseq_ffmpeg(path):
    """
    Transforms an image sequence file to a format
    compatible with ffmpeg image2 demux
    Will return the original path if no image index has been found
    """
    head, tail = os.path.split(path)
    for i in range(8, 0, -2):
        regex = re.compile(r"\d{" + str(i) + "}")
        match = regex.search(tail)
        if match:
            output = f"%0{i}d".join(tail.split(match[0]))
            return os.path.join(head, output)
    return path


def create_chunk_filename(path):
    """
    Converts an image sequence file path to one suitable
    for a chunk
    :path: str - path to one frame of the img seq
    :return: str - path to the chunk file
    """
    head, tail = os.path.split(path)
    for i in range(8, 0, -2):
        regex = re.compile(r"\d{" + str(i) + "}")
        match = regex.search(tail)
        if match:
            output = tail.split(match[0])[0] + "_#IFRAME#.mp4"
            return os.path.join(head, output)
    return path + "_#IFRAME#.mp4"


def get_imgseq_framerange(path):
    """
    Deduces the framerange of the given image sequence
    :path: str - path to one frame of the img seq
    :return: tuple of int - (start, end)
    """
    dir_name, file_name = os.path.split(path)
    for i in range(8, 0, -2):
        regex_index = re.compile(r"\d{" + str(i) + "}")
        match = regex_index.search(file_name)
        if match:
            head, tail = file_name.split(match[0])
            regex_file = re.compile("".join([head, r"\d{", str(i), "}", tail]))
            indexes = [regex_index.search(file)[0]       # Only indexes
                       for file in os.listdir(dir_name)  # For every file
                       if regex_file.match(file)]        # In the img seq
            return int(min(indexes)), int(max(indexes))


def main(input_path, fps, crf, chunk):
    input_path = os.path.abspath(input_path)
    shot_name = os.path.basename(input_path)
    job_name = "dpx_to_mov"
    show_name = "testing"
    user = getpass.getuser()
    outline = Outline(job_name, shot=shot_name, show=show_name, user=user)

    # Create the MakeMov Layer
    layer_name = "seq_to_mov"
    threads = 1.0
    threadable = False
    frame_start, frame_end = get_imgseq_framerange(input_path)
    range_len = frame_end - frame_start
    frame_range = str(frame_start) + "-" + str(frame_end)
    input_path_ffmpeg = translate_imgseq_ffmpeg(input_path)
    output_chunk_path = create_chunk_filename(input_path)

    seqtomov_layer = SeqToMov(layer_name, chunk=chunk, threads=threads,
                              range=frame_range, threadable=threadable,
                              crf=crf, fps=fps)
    seqtomov_layer.add_input("main", input_path_ffmpeg)
    seqtomov_layer.add_output("main", output_chunk_path)

    outline.add_layer(seqtomov_layer)

    # Submit job
    cuerun.launch(outline, use_pycuerun=False)


if __name__ == '__main__':
    args = get_args()
    main(args.input_path, args.fps, args.crf, args.chunk)
