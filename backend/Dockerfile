FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install -y python3 python3-pip python3-dev build-essential
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN ln -s /usr/bin/pip3 /usr/bin/pip

COPY . /backend
WORKDIR /backend

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8989
CMD ["python", "app.py"]