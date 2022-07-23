# from ubuntu
FROM ubuntu:20.04
RUN apt-get update

# install nginx for rtmp
RUN apt-get install -y build-essential libpcre3 libpcre3-dev libssl-dev
RUN apt-get install -y wget
RUN apt-get install -y unzip

RUN wget http://nginx.org/download/nginx-1.18.0.tar.gz
RUN tar -xf nginx-1.18.0.tar.gz
RUN wget https://github.com/arut/nginx-rtmp-module/archive/master.zip
RUN unzip master.zip
RUN mv nginx-rtmp-module-master nginx-rtmp-module

RUN apt-get install -y zlib1g zlib1g-dev
WORKDIR /nginx-1.18.0
RUN ./configure --with-http_ssl_module --add-module=/nginx-rtmp-module
RUN make -j 1
RUN make install

# RUN echo $(ls /nginx-1.18.0/conf)

# install for ffmpeg
# RUN mkdir /ffmpeg_sources
# WORKDIR /ffmpeg_sources
# # RUN apt-get install -y libx264 libfdk-aac
# RUN git -C x264 pull 2> /dev/null || git clone --depth 1 https://git.videolan.org/git/x264 && \
#     cd x264 && \
#     PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --enable-static --enable-pic && \
#     PATH="$HOME/bin:$PATH" make && \
#     make install

RUN apt-get install -y ffmpeg

# run nginx
WORKDIR /nginx-1.18.0
# RUN echo $(ls)
# COPY ./conf/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY ./conf/nginx.conf /nginx-1.18.0/conf/nginx.conf
CMD ["nginx", "-g", "daemon off;"]

EXPOSE 80