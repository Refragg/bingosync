FROM python:3.7-bullseye
RUN mkdir ws
WORKDIR /ws
ADD ./requirements.txt requirements.txt
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8888
