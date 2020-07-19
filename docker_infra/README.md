# Docker testing infrastructure

This quick start infrastructure has been built from the [OpenCue Sandbox environment](https://github.com/AcademySoftwareFoundation/OpenCue/tree/master/sandbox). The official documentation can be found [here](https://www.opencue.io/docs/quick-starts)

To deploy, make sure you have a docker daemon running, then export the two following environment variables :
```bash
export CUE_FRAME_LOG_DIR=/tmp/rqd/logs
export POSTGRES_PASSWORD=<REPLACE-WITH-A-PASSWORD>
```

If you prefer, you can declare them in a `.env` file.

Then, build the images and deploy the environment.
```bash
docker-compose build
docker-compose up
```
## Differences from the original sandbox

The component that I've changed the most from the OpenCue sandbox is the rqd container.

Rqd is the rendering node of the infra, usually you have a lot more than one.
Here, since I'm mostly working with ffmpeg, I've just installed ffmpeg and various requirements on it.

If you want to test other applications, make sure the host that runs rqd has access to them.
Link to the doc [here](https://www.opencue.io/docs/other-guides/customizing-rqd/).
