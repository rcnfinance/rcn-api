FROM python:3.6

RUN apt-get update && apt-get install -y build-essential

ADD src /project
ADD requirements.txt /project
WORKDIR /project
RUN pip install -r requirements.txt
