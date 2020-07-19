## rqd with ffmpeg amd64
FROM opencue/rqd

RUN yum -y update
RUN yum -y install wget
RUN yum clean all

RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz
RUN wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz.md5
RUN md5sum -c ffmpeg-git-amd64-static.tar.xz.md5

RUN tar xvf ffmpeg-git-amd64-static.tar.xz --strip-components=1 "*/ffmpeg"
RUN rm -f ffmpeg*.tar.xz*
RUN mv ffmpeg /usr/local/bin

RUN mkdir -p /usr/local/share/model
RUN wget https://raw.githubusercontent.com/Netflix/vmaf/master/model/vmaf_v0.6.1.pkl
RUN wget https://raw.githubusercontent.com/Netflix/vmaf/master/model/vmaf_v0.6.1.pkl.model
RUN mv vmaf_v0.6.1.pkl* /usr/local/share/model/