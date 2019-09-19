# abcm-checkindesk

Creator :    Guillaume

Maintenance: Rom1

Requirements : 
* Apache 2.x
* Mongodb for persistence

## Configuration
Ancienne configuration. A modier pour Docker
### Apache Virtualhost : 
<Directory /var/www/ndm/>
        AuthType Basic
        AuthName "Autorisation requise"
        AuthUserFile htndm.pwd
        Require user ndm bolo
</Directory>


<VirtualHost *:80>
        ServerName "<changeme>"
        DocumentRoot /var/www/ndm
        ErrorLog /var/log/apache2/ndm<changeme>.error.log
        CustomLog /var/log/apache2/ndm<changeme>.log common
</VirtualHost>

### Mongo php driver:
pecl install mongo

### PHP.ini:
short_open_tag = On

extension=mongo.so

## ToDo List
* Faire un page pour visualiser les statistiques
* Migrer ver PHP7
* Migrer dans un container alpine

## Change Log
* Adaptation pour Docker (Rom1)
* Création (Guillaume)
