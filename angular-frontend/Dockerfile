FROM node:14.1.0-stretch-slim

WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH	
COPY package.json /app/package.json
RUN npm install
RUN npm install -g @angular/cli@7.3.9

COPY . /app


CMD ng serve --proxy-config proxy.conf.json --host 0.0.0.0










