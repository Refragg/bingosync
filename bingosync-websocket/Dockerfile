FROM python:3.7-bullseye
RUN mkdir ws
WORKDIR /ws
ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8888
