# Making sense of submission scripts with Pyoutline

## Blessed by a youtube video

The documentation of Opencue mentions the concept of outline scripts as a tool to submit jobs to Cuebot. It also mentions the library PyOutline as the python library that achieves this goal, and that Cuesubmit is just a GUI on top of it.

That's certainly a good start, but other than that, I didn't have a lot of information on how to get started with this. I checked the code inside of the Pyoutline library, the samples as well, but didn't understand where to start from, i.e. how to build a basic submission script.

I started browsing the mailing list, the github issues. After following a series of links, I fell onto the recording of a meetup in which people from Sony pictures talk about the history of Cue and the genesis of the Opencue project, and engineers from Google explain their work on the project. The meetup includes a demo in which the jobs are not launched via Cuesubmit, but with outline scripts and the code is on screen !

The interesting part is around [1:04](https://youtu.be/Vh6wtTzEj_E?t=3848), but if you are interested I suggest [watching the whole thing](https://www.youtube.com/watch?v=Vh6wtTzEj_E).

So after watching this, I did a bunch of screenshots and started working on scripts.

## The structure of an outline script

## Adding extra steps (dependencies)

## Dividing layers into multiple frames, with a bit of added difficulty