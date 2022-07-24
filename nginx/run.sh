docker build -t nginx --progress=plain .
docker run --name nginx -d -p 8080:8080 -p 1935:1935 nginx