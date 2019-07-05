FROM nginx:1.17-alpine

ENV NGINX_HOME /etc/nginx/
ENV NGINX_HTML_HOME /usr/share/nginx/html/

COPY build ${NGINX_HTML_HOME}
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf ${NGINX_HOME}/conf.d/
COPY nginx.conf ${NGINX_HOME}/nginx.conf

CMD ["nginx", "-g", "daemon off;"]