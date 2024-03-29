#!/bin/bash

CID_CONFIGFILE="/var/www/html/config.default.inc.php"

set -e
trap "echo SIGNAL" HUP INT QUIT KILL TERM

if [ -n "${CID_USER}" ]
then
  sed -i "s^\(.*'DB_USER'.*'\).*\('.*\)^\1${CID_USER}\2^" ${CID_CONFIGFILE}
fi

if [ -n "${CID_PWD}" ]
then
  sed -i "s^\(.*'DB_PWD'.*'\).*\('.*\)^\1${CID_PWD}\2^" ${CID_CONFIGFILE}
fi

if [ -n "${CID_PORT}" ]
then
  sed -i "s^\(.*'DB_PORT'.*'\).*\('.*\)^\1${CID_PORT}\2^" ${CID_CONFIGFILE}
fi

if [ -n "${CID_HOST}" ]
then
  sed -i "s^\(.*'DB_HOST'.*'\).*\('.*\)^\1${CID_HOST}\2^" ${CID_CONFIGFILE}
fi

if [ -n "${CID_DB}" ]
then
  sed -i "s^\(.*'DB_NAME'.*'\).*\('.*\)^\1${CID_DB}\2^" ${CID_CONFIGFILE}
fi

if [ -n "${CID_COLLECTION}" ]
then
  sed -i "s^\(.*'COL_NAME'.*'\).*\('.*\)^\1${CID_COLLECTION}\2^" ${CID_CONFIGFILE}
fi

if [ -n "${CID_DATE}" ]
then
  mongo_format=$(echo ${CID_DATE} | awk 'BEGIN{FS="/"}{printf "%d/%d/%d",$3,$2,$1}')
  year=$(echo ${CID_DATE} | cut -d'/' -f3)
  sed -i "s^\(.*'INFOS'.*'DATE'.*'\).*\('.*\)^\1${mongo_format}\2^" ${CID_CONFIGFILE}
  sed -i "s^\(.*'HEADER_TITLE'.*\)2015\(.*\)^\1${year}\2^" ${CID_CONFIGFILE}
  sed -i "s^\(.*'FOOTER'.*\)2015\(.*\)^\1${year}\2^" ${CID_CONFIGFILE}
fi

if [ "$1" = "apache2" ]
then
	exec /usr/sbin/apache2 -D FOREGROUND
fi

exec "$@"
