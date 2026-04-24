FROM nginx:latest

COPY ./build /var/www
COPY nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]