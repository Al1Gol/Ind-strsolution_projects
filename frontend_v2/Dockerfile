FROM nginx:latest

COPY ./build /var/www
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 800
CMD ["nginx", "-g", "daemon off;"]