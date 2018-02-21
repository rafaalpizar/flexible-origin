# Flexible Origin Instalation Procedure with Apache2

0. OS

> uname -a
Linux ip-172-31-36-246 3.13.0-141-generic #190-Ubuntu SMP Fri Jan 19 12:52:38 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

```
$ cat /etc/*release*
DISTRIB_ID=Ubuntu
DISTRIB_RELEASE=14.04
DISTRIB_CODENAME=trusty
DISTRIB_DESCRIPTION="Ubuntu 14.04.5 LTS"
NAME="Ubuntu"
VERSION="14.04.5 LTS, Trusty Tahr"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 14.04.5 LTS"
VERSION_ID="14.04"
HOME_URL="http://www.ubuntu.com/"
SUPPORT_URL="http://help.ubuntu.com/"
BUG_REPORT_URL="http://bugs.launchpad.net/ubuntu/"
```


1. Install Packages
   ```
    sudo aptitude install apache2 python3.4 python3.4-venv python-virtualenv libapache2-mod-wsgi-py3
   ```

2. Create directories
   ```
    $ sudo chgrp ubuntu /srv
    $ sudo chmod g+w /srv
    $ mkdir /srv/flexible_origin{,_venv}
   ```

3. Change directory ownership to regular user ( "ubuntu" as example )
   ```
    $ sudo chown -R ubuntu:ubuntu /srv/flexible_origin*
   ```

4. Install Python Virtual Environment
   ```
    $ virtualenv -p python3 /srv/flexible_origin_venv/
   ```

5. Install Flask
   ```
    $ . /srv/flexible_origin_venv/bin/activate
    (flexible_origin_venv) $ pip install flask
    (flexible_origin_venv) $ deactivate
   ```

6. Copy source code to server - External Machine (Optional)
   ```
    $ tar --exclude .git/ --exclude .gitignore --exclude venv/ --exclude README.md~ --exclude __pycache__/ --exclude *# --exclude static/fo.log --exclude user/ -czvf /tmp/flexible_origin_src.tar.gz .
    $ scp /tmp/flexible_origin_src.tar.gz ubuntu@machine:/home/ubuntu/
    It is required to manually create "user" directory in server
   ```

7. Expand the source code to server destination
   ```
    $ tar -xzf /home/ubuntu/flexible_origin_src.tar.gz -C /srv/flexible_origin
   ```

8. TLS Self-Sing Cerficate
   ```
    $ mkdir /srv/tls_certs/
    $ sudo chown ubuntu:ubuntu /srv/tls_certs/
    $ openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /srv/tls_certs/privkey.pem -out /srv/tls_certs/cert.pem
   ```

9. Apache modules enable
   ```
    $ a2enmod wsgi ssl
    $ service apache2 stop
    $ service apache2 start
   ```

10. WSGI Flexible Origin Setup

  - Check the file contents 'flexorigin.wsgi'
    ```
    python_home = '/srv/flexible_origin_venv'

    activate_this = python_home + '/bin/activate_this.py'
    with open(activate_this) as file_:
        exec(file_.read(), dict(__file__=activate_this))

    import sys
    sys.path.insert(0,  '/srv/flexible_origin')
    from flexorigin import app as application
    ```

11. Apache ports configuration
    ```
     Listen 80
     <IfModule ssl_module>
	     Listen 443
     </IfModule>
     <IfModule mod_gnutls.c>
	     Listen 443
     </IfModule>
    ```

12. Apache VHost configuration
    ```
     # Python virtual environment
     WSGIDaemonProcess flexorigin user=ubuntu group=ubuntu threads=5

     <VirtualHost *:80>
       ServerName ec2-54-174-117-235.compute-1.amazonaws.com
       ServerAdmin webmaster@localhost
       DocumentRoot /var/www/html

       WSGIScriptAlias / /srv/flexible_origin/flexorigin.wsgi
       <Directory "/srv/flexible_origin">
	 WSGIProcessGroup flexorigin
	 WSGIApplicationGroup %{GLOBAL}
	 AllowOverride None
	 Options FollowSymLinks
	 Require all granted
       </Directory>

       ErrorLog ${APACHE_LOG_DIR}/fo-error.log
       CustomLog ${APACHE_LOG_DIR}/fo-access.log combined
     </VirtualHost>

     <IfModule mod_ssl.c>
       <VirtualHost *:443>
	 ServerAdmin webmaster@localhost
	 DocumentRoot /var/www/html
	 ServerName ec2-54-174-117-235.compute-1.amazonaws.com
	 ErrorLog ${APACHE_LOG_DIR}/fo-error.log
	 CustomLog ${APACHE_LOG_DIR}/fo-access.log combined

	 WSGIScriptAlias / /srv/flexible_origin/flexorigin.wsgi
	 <Directory "/srv/flexible_origin">
	   WSGIProcessGroup flexorigin
	   WSGIApplicationGroup %{GLOBAL}
	   AllowOverride None
	   Options FollowSymLinks
	   Require all granted
	 </Directory>

	 SSLEngine on
	 SSLCertificateFile	/srv/tls_certs/cert.pem
	 SSLCertificateKeyFile	/srv/tls_certs/privkey.pem

	 <FilesMatch "\.(cgi|shtml|phtml|php)$">
	   SSLOptions +StdEnvVars
	 </FilesMatch>
	 <Directory /usr/lib/cgi-bin>
	 SSLOptions +StdEnvVars
       </Directory>
       BrowserMatch "MSIE [2-6]" \
       nokeepalive ssl-unclean-shutdown \
       downgrade-1.0 force-response-1.0
       BrowserMatch "MSIE [17-9]" ssl-unclean-shutdown
     </VirtualHost>
     </IfModule>
    ```

