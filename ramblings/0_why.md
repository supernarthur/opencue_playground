# Why did I started to tinker with this ?

Like Nick Offerman in Devs, you might think that the universe is deterministic. That we all are gliding on our tram lines. Everything we do at T, we do because of the situation at T-1.

Well, I have no idea.

But I think some context may be a simple way of answering the big bold question up top.

## Some context, then

We are in the summer of 2020. Job A finished mid-april, Job B was supposed to follow quickly, but the 'rona said no.
The first weeks are nice. I rest, read, watch series. But after a while, I start to think that maybe it would be a good idea to make sure I use this time to work on something useful.

My line of work is postproduction engineering. It's a nice jack-of-all-trades job. I know a bit about systems, coding, and video. Python is the de-facto language of a lot of APIs in this field. I am not very good at it from a developper perspective, but I know a few tricks. So I set the objective to improve on this aspect during the summer.

But, and there is a but : I need a problem to solve. I am not very good at building things from scratch, and I can't learn anything if there is not a project behind.

## A word about Atlas

Atlas is pretty great. It's one of the nice projects I've seen come to life at Job A (I've mostly watched everything from the side, I was working on other stuff). It was a Telestream Lightspeed server running Vantage on it, with the main purpose of automating the creation of client links.

Basically, when someone would need to export something from its workstation (during editing, color, or finishing), they would export it to Atlas' shared storage in high quality (usually DPX of Prores), and the server would pick the files up, create a H264 version, copy everthing at the right place for in-house use (and long-term archiving). After that, it would also upload it to our client viewing platform, and send a mail to the project manager with a link to it.

A great solution to a nice problem. Pretty pricy though. And I don't remember very well, but I'm sure at some point we've talked about studios doing everything with opensource solutions, mainly ffmpeg and some pipeline automation.

A good thing about watching a project like this, you see pretty much everything that goes wrong. I also had the time to discuss with my colleagues about what changes in design would be a good idea in retrospect. 
In Atlas' case, one problematic area was the starting point of a job, by watching a folder. The system was a bit overwhelmed by all the folders it had to check (a few per project, so in the 3 digits area), and since some jobs failed to launch at times, the users had to double check to make sure the job would start.

One of the ways we wanted to solve that was to export high resolution media on the production servers, and just tell Atlas to launch the job via a call to an API or something.

So, that was my starting point. Make an application which waits for an API call of some kind to launch a ffmpeg command on some file that sits on a shared storage. And then have a way of easily monitoring job progress.

## ~~Reading~~Procrastinating

To make such an app, I figured there is two components to learn about : a way to make an API and a small website in python, and how ffmpeg works. But instead of trying stuff up, I mostly read on the subject for a while, starting with ffmpeg.

The official ffmpeg wiki has good articles about [H264](https://trac.ffmpeg.org/wiki/Encode/H.264) and the usage of [ffmpeg in VFX applications](https://trac.ffmpeg.org/wiki/Encode/VFX). I also fell onto [ffmprovisr](https://amiaopensource.github.io/ffmprovisr), an "in practice" guide that shows a lot of the features of the software.

It was kind of difficult to know how to dial in the quality of the encoding, so I did some research on what settings were considered the best quality/weight ratio. I fell onto [people](https://eposvox.com/post/x264-is-not-worth-it--a-bad-benchmark--gn-follow-up-image-quality-analysis) [automating](https://streamquality.report/docs/report.html) the verification process of the encoding using various libraries. The most interesting library so far is [VMAF](https://github.com/Netflix/vmaf), which has been developped by Netflix to assess video quality in a perceptual way.

It was pretty cool to imaging batching dozens of compression jobs with different settings and wait for a program to tell me which ones had the better quality.

## The benefit of not doing anything for a while (a personal take on [hammock-driven development](https://www.youtube.com/watch?v=f84n5oFoZBc))

On the app side, I was half-sold on making up something with Flask. But the perspective of having to do some kind of front-end dev wasn't particularly driving. I was also reading about energy preservation, ecology, not buying too much stuff. I was wondering how to make an idea like this work on machines that you already have available in a post-production facility, like workstations.

Than it hit me : just like VFX studios, I could do _all this_ with some kind of render manager. A bit of research and I fell on OpenCue. The idea matured into something like this :

- Learn about how OpenCue work (if I hit a wall at some point, find something else).
- Deploy some kind of testing infrastructure, if possible on my laptop. If I can learn a thing or two about Docker, that's a bonus.
- Find a way to submit ffmpeg jobs on my test render farm.
- Think of other things to test in the process. If they are stupid and/or useful, bonus points.