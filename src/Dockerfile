FROM php:5-apache

LABEL maintainer="Rom1 <rom1@canel.ch> - CANEL - https://www.canel.ch"
LABEL date="2019-09-09"
LABEL description="BOLO: Compteur de visiteurs pour la NdM"

RUN apt-get update && apt-get install -y libssl-dev \
         && pecl install mongo \
         && docker-php-ext-enable mongo

ENV TZ Europe/Zurich

COPY ./www /var/www/html
