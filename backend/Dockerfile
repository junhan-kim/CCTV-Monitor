FROM ubuntu:18.04

COPY . /backend
WORKDIR /backend
RUN pip install -r requirements.txt

EXPOSE 8989
CMD ["python", "app.py"]