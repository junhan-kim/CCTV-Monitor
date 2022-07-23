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

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y ffmpeg

# run nginx
COPY ./conf/nginx.conf /usr/local/nginx/conf/nginx.conf
CMD ["/usr/local/nginx/sbin/nginx", "-g", "daemon off;"]

EXPOSE 80