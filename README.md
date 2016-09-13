abcm-checkindesk
----------------

Author : Guillaume

Requirements : 

o Apache 2.x
o Mongodb for persistence

Apache Virtualhost : 
--------------------
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


