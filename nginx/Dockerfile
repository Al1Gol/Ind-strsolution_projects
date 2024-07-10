FROM nginx:1.25-alpine

# apline based = ubuntu => apk istead apt
RUN apk update && apk add openssl
RUN rm /etc/nginx/conf.d/default.conf && mkdir -p /home/web/www
 
RUN openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048 &&\
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/certs/self.key -out /etc/ssl/certs/self.crt \
    -subj "/C=RU/ST=Stavropolskyi kray/L=Stavropol/O=Indsol/OU=Org/CN=5.182.4.206"


COPY nginx.conf /etc/nginx/conf.d
COPY ssl-params.conf /etc/nginx/ssl-params.conf
