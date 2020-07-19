# Submit scripts

Here you'll find libs and scripts to submit various jobs to opencue.

You must have access to OpenCue client libraries to make them work. Check [this](https://github.com/Supernarthur/opencue_playground/README.md#setup-the-client-apps-and-libraries) to install them.

## Contents / Usage

- `simple_compress.py file` : Basic ffmpeg x264 compression of a file into `file_H264.mp4`
- `check_compression.py file ref_file` : Use the vmaf library to perceptually compare `file` to `ref_file` 
- `simple_compress.py file crf` : Basic ffmpeg x264 compression of a file into `file_H264.mp4`, then checks it against the source using vmaf. `crf` is a x264 parameter that controls the quality of the compression. See [here](https://trac.ffmpeg.org/wiki/Encode/H.264) if you want to learn more about this parameter.
