docker build -t nginx --progress=plain .
docker run --name nginx -d -p 8080:80 nginx