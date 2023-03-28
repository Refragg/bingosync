FROM python:3.7-bullseye

# Note: bingosync uses the 'node' command, this means we need to install node
RUN apt-get update && apt-get install -y \
    software-properties-common \
    npm
RUN npm install npm@latest -g && \
    npm install n -g && \
    n latest


RUN mkdir app
WORKDIR /app
ADD ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir logs
COPY . .
EXPOSE 8000
