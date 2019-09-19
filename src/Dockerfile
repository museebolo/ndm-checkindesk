FROM canelrom1/apache2:debian10

LABEL maintainer="Rom1 <rom1@canel.ch> - CANEL - https://www.canel.ch"
LABEL date="09/09/2019"
LABEL description="BOLO: Compteur de visiteurs pour la NdM"

RUN wget -q https://packages.sury.org/php/apt.gpg -O- | apt-key add - \
 && echo "deb https://packages.sury.org/php/ stretch main" > /etc/apt/sources.list.d/php.list \
 && apt-get update && apt-get upgrade -y

RUN apt-get install -y libapache2-mod-php5.6 \
                       php5.6 \
                       php5.6-dev \
                       php-mongo

COPY ./conf/php.ini /etc/php/5.6/apache2/php.ini

ENV TZ Europe/Zurich

RUN rm -fr /var/www/html
COPY ./www /var/www/html
RUN chown www-data:www-data -R /var/www/html

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["apache2"]
