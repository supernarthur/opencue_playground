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
from modules.ffmpeg import SeqToMov, ConcatMov
from outline import Outline, cuerun


def get_args():
    """
    Parse arguments
    """
    parser = argparse.ArgumentParser(description="Submits a job to OpenCue")
    parser.add_argument("input_path", type=str,
                        help=("path to the input image sequence "
                              "(first frame)"))
    parser.add_argument("-f", "--fps", type=float, metavar="fps", default=25,
                        help="framerate of the desired output")
    parser.add_argument("-q", "--crf", type=int, metavar="crf", default=25,
                        help="quality of the output (see ffmpeg/x264 crf)")
    parser.add_argument("-c", "--chunk", type=int, metavar="chunk",
                        default=600,
                        help="size in frames of the render chunks")
    parser.add_argument("-o", "--output", type=str,
                        help="The path to the output file")
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


def create_chunk_path_template(path):
    """
    Converts an image sequence file path to one suitable
    for a chunk file being processed by cuebot
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


def get_chunk_paths(chunk_path_template, chunk, frame_start, frame_end):
    """
    Gets a list of the actual chunks paths created by opencue for later
    combination
    :chunk_path_template: str - path given to cuebot (with #IFRAME#)
    :chunk: int - chunk length in frames
    :frame_start: str - first frame of the img seq
    :frame_end: str - last frame of the img seq
    """
    index_length = len(frame_start)
    return [chunk_path_template.replace("#IFRAME#", str(chunk_start))
            for chunk_start in range(int(frame_start), int(frame_end), chunk)]


def get_imgseq_framerange(path):
    """
    Deduces the framerange of the given image sequence
    :path: str - path to one frame of the img seq
    :return: tuple of str - (start, end)
        we stay in str to avoid losing zfilled indexes
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
            return min(indexes), max(indexes)


def main(input_path, fps, crf, chunk, output_path):
    """
    Sends a job to opencue that will compress an image sequence to
    an H.264 file using multiple render nodes in parallel
    :input_path: str - path to the first frame of the image sequence
    :fps: float - framerate of the desired encoded file
    :crf: int - quality of the desired encoded file

    """
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
    range_len = int(frame_end) - int(frame_start)
    frame_range = frame_start + "-" + frame_end
    input_path_ffmpeg = translate_imgseq_ffmpeg(input_path)
    output_chunk_path_template = create_chunk_path_template(input_path)

    seqtomov_layer = SeqToMov(layer_name, chunk=chunk, threads=threads,
                              range=frame_range, threadable=threadable,
                              crf=crf, fps=fps)
    seqtomov_layer.add_input("main", input_path_ffmpeg)
    seqtomov_layer.add_output("main", output_chunk_path_template)

    outline.add_layer(seqtomov_layer)

    # Create the ConcatMov Layer
    layer_name = "concat_mov"
    concatmov_layer = ConcatMov(layer_name, chunk=1, threads=threads,
                                range=1, threadable=threadable)
    chunk_paths = get_chunk_paths(output_chunk_path_template,
                                  chunk, frame_start, frame_end)
    for chunk_path in enumerate(chunk_paths):
        concatmov_layer.add_input("", chunk_path)
    concatmov_layer.add_output("main", output_path)
    concatmov_layer.depend_all(seqtomov_layer)

    outline.add_layer(concatmov_layer)

    # Submit job
    cuerun.launch(outline, use_pycuerun=False)


if __name__ == '__main__':
    args = get_args()
    main(args.input_path, args.fps, args.crf, args.chunk, args.output)
