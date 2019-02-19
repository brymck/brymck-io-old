FROM node:8-alpine as builder

RUN apk update && apk add --no-cache ca-certificates git && update-ca-certificates

WORKDIR /usr/src/app
COPY package.json yarn.lock ./
RUN yarn install
COPY .env tsconfig.json ./
COPY public public
COPY src src
RUN yarn build

# Deploy static files using nginx
FROM nginx:alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /usr/src/app/build /var/www

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
