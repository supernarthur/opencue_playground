# OpenCue Playground

This is the result of a personal exploration of OpenCue as a rendering system to dispatch video-oriented
jobs (compression and analysis using ffmpeg). 

You can read my ramblings on why I worked on this and what I've learned in the appropriate section.

Most of the tests have been ran using my mac as a client, with the infrastructure running in docker.

## How to run

### Setup the opencue intrastructure in docker

See the appropriate documentation [here](https://github.com/Supernarthur/opencue_playground/tree/master/docker_infra).

### Setup the client apps and libraries

There is more than one component on the client side. Everything can be installed following the documentation
on the official website.

Here are the steps :

- Clone the repo
- [Install the libraries](https://www.opencue.io/docs/getting-started/installing-pycue-and-pyoutline/) (PyCue and PyOutline)
- [Install CueGUI](https://www.opencue.io/docs/getting-started/installing-cuegui/)
- [Install CueSubmit](https://www.opencue.io/docs/getting-started/installing-cuesubmit/) (optional, but a good way to test stuff)
- [Install CueAdmin](https://www.opencue.io/docs/getting-started/installing-cueadmin/) (optional)

### Test my stuff

The client libraries will be installed in a python virtualenv. 
Use this virtualenv to launch pretty much every python script that you'll find in this repo.
