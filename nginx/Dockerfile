# from ubuntu
FROM ubuntu:20.04
RUN apt-get update

# install nginx for rtmp
RUN apt-get install -y build-essential libpcre3 libpcre3-dev libssl-dev
RUN wget http://nginx.org/download/nginx-1.14.0.tar.gz
RUN tar -xf nginx-1.14.0.tar.gz
RUN cd nginx-1.14.0
RUN ./configure --with-http_ssl_module --add-module=../nginx-rtmp-module
RUN make -j 1
RUN make install

COPY conf/nginx.conf /etc/nginx/conf.d/nginx.conf

CMD ["nginx", "-g", "daemon off;"]

EXPOSE 80