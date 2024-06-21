FROM node:19-alpine AS builder

WORKDIR /app

COPY package.json ./
COPY yarn.lock ./

RUN yarn install

COPY . .

RUN yarn run build

FROM nginx:1.23.2-alpine AS server

ARG PORT=3000
ENV PORT=$PORT

EXPOSE $PORT 

COPY --from=builder ./app/build /usr/share/nginx/html
COPY deploy/nginx.conf /etc/nginx/conf.d/default.conf

CMD ["nginx", "-g", "daemon off;"]