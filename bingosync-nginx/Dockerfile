FROM nginx:1.23-alpine

ARG SSL_CERT_FILE
ARG SSL_CERT_KEY

ENV SSL_CERT_FILE $SSL_CERT_FILE
ENV SSL_CERT_KEY $SSL_CERT_KEY

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN sed -i "s/SSL_CERT_FILE/${SSL_CERT_FILE}/" /etc/nginx/conf.d/nginx.conf
RUN sed -i "s/SSL_CERT_KEY/${SSL_CERT_KEY}/" /etc/nginx/conf.d/nginx.conf
