# Getting familiar with the infrastructure

To start playing with the app, I had to deploy it somehow. Fortunately, this part is well documented, and a lot of the heavy lifting has already been done by the developers.

## A quick overview

![infra overview](https://www.opencue.io/docs/images/opencue_architecture.svg)

Most of what I'm gonna say here is a paraphrase of [this article](https://www.opencue.io/docs/concepts/opencue-overview/) in the documentation.

### Cuebot and its DB

Cuebot is the scheduler. It will receive render queries from the artists, admin commands from the technical staff (render wrangler or IT) and will process them.

All of the job information is stored inside of its database which was originally based on oracle but is moving to postgresql.

### The render daemon : rqd

On every machine that can be used to render jobs, there will be rqd running on it. Rqd will connect to Cuebot when launched and will wait for jobs to be dispatched to it.

The progress is periodically sent to Cuebot until it finishes or fails. At that point it sends this last info to Cuebot and becomes available again.

You can start only with one node, but as any render farm, you can easily scale up to many nodes. A small studio will have a 2 to 3 digits count of render nodes, but the bigger ones can go to the 4 digits realm.

### The client libraries : pycue and pyoutline

This is your API to discuss with Cuebot. You can get information about the farm, you can send jobs to the farm, and you can administrate it.

Everything is written in python, which is the standard in many studio pipelines. That makes Opencue easier to interface with pre-existing pipeline.
Although the functions themselves are well documented, I had some trouble understanding how all the objects, functions, methods and so on fit together. This will be the subject of the next rambling.

There are also useful GUI tools included, which use the python API. CueSubmit is a good way to kickstart your first jobs and learn about the different parameters. CueGUI is the dashboard that you can use to monitor your rendering infrastructure, the progress of your jobs, etc.

## The sandbox environment 

In the official documentation, the [quick-start](https://www.opencue.io/docs/quick-starts/) article helps you spin-up the infrastructure using docker-compose. The containers it will generate are :

- Cuebot
- Cuebot's postgresql database
- A temporary Flyway application that sets up the database schema
- A centos linux with rqd installed

When you have everything running, you can setup a virtualenv on your machine to install the client libraries.

This setup is pretty bare-bones, but you already have access to all of the logic of OpenCue. That is enough to launch one or two test jobs using CueSubmit.

### Adding software and features to your rqd container(s)

Since I wanted to work with ffmpeg, I needed to install it on the rqd container. The documentation has page on [customizing the rqd container](https://www.opencue.io/docs/other-guides/customizing-rqd/) using blender as an example.

For ffmpeg, I could install it using the rpmfusion repositories. That is what I did at first, but the version of ffmpeg that is available on this repo is not compiled with vmaf, which I wanted to use.

That is why I instead used the ffmpeg static builds, and added the vmaf models from their github repositories.

### Not exactly a best practice

From what I understood about building infrastructure with docker, the way I fetch a static build is not really best practice. The link to the build can point to a different version of ffmpeg so two images built at different times have a high chance of using a different build of ffmpeg.

Another method would be to compile ffmpeg and the libraries I need in the container. Using environment variables, I could then point to the exact version of ffmpeg and its libraries and have a container that is 100% replicable.

I chose to stay with the static build for my tests, because I was a bit limited in computing power and internet bandwidth. But at some point I want to try to have something replicable, so I may try this.

## So where are we now ?

At this point, having OpenCue infra running, I submitted a few ffmpeg commands using CueSubmit. I had to figure out what kind of jobs would I want to create, so after a bit of tinkering, I drafted a small progression of job types :

- A simple compression from a mov file to a H.264 .mp4
- A vmaf check of a compressed file against a reference file
- Doing both of those one after the other so you can have an idea of the impact of the compression (that was a good way of learning about dependancies between the steps of a job)
- Maybe make all of this work with a DPX sequence with a separate audio file (that can be a cool way of introducing jobs that work on a fraction of the files, so the work can be distributed on multiple rqd hosts)

Obviously, submitting complex jobs like this through CueSubmit wouldn't be practical in production. So I had to learn about the pyOutline library to make anything work.

