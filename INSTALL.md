# MISP-RPM

This document is specifically written for RHEL 7.x install;
please follow the MISP upstream official documentation for anything MISP
related.

The main differences with a regular MISP installed are around RHEL software
collection specifics and packaging

# Enable RHEL subscription and software collections

```bash
sudo subscription-manager register --auto-attach
sudo yum-config-manager --enable rhel-server-rhscl-7-rpms
sudo subscription-manager repos --enable rhel-7-server-optional-rpms
sudo yum install -y ca-certificates
```

## Install Apache webserver - httpd24

<<<<<<< HEAD
```bash
sudo yum install -y httpd24 httpd24-mod_ssl
sudo systemctl enable httpd24-httpd
sudo systemctl restart httpd24-httpd
=======
```
yum install misp misp-python-virtualenv misp-modules
>>>>>>> history
```

## Install PHP - rh-php73

```
sudo yum install -y rh-php73
```

Set up recommended max values for PHP runtime
`/etc/opt/rh/rh-php73/php.ini`
```
- max_execution_time = 30
+ max_execution_time = 300
- memory_limit = 128M
+ memory_limit = 2048M
- post_max_size = 8M
+ post_max_size = 50M
- upload_max_filesize = 2M
+ upload_max_filesize = 50M
```

## Installing packages

Follow the install order and adapt versions if required
```
# prereq for misp
sudo yum install -y gtcaca-1.0+*.rpm libcaca*.rpm imlib2*.rpm
sudo yum install -y faup-1.6.0+*.rpm
sudo yum install -y ssdeep-libs*.rpm
sudo yum install -y libbrotli*.rpm
sudo yum install -y misp-php73-*rpm

# install misp rpm
sudo yum install -y misp-python-virtualenv-2.4.*.rpm misp-2.4.*.rpm
```

## Apache/httpd configuration

Example Apache VirtualHost configuration:

`/opt/rh/httpd24/root/etc/httpd/conf.d/misp.conf`
```xml
<VirtualHost _default_:80>
    DocumentRoot /var/www/MISP/app/webroot
    <Directory /var/www/MISP/app/webroot>
        Options -Indexes
        AllowOverride all
        Require all granted
    </Directory>

    LogLevel warn
    ErrorLog /var/log/httpd24/misp_error.log
    CustomLog /var/log/httpd24/misp_access.log combined

    ServerSignature Off

    Header always set X-Content-Type-Options nosniff
    Header always set X-Frame-Options SAMEORIGIN 
    Header always unset "X-Powered-By"
</VirtualHost>
```

`sudo systemctl restart httpd24-httpd` after configuration change

## Install MySQL databse - rh-mariadb105-mariadb

```bash
sudo systemctl enable rh-mariadb105-mariadb.service
sudo systemctl start rh-mariadb105-mariadb.service
```

Create database, user and grant privileges. 
First command should open a MySQL shell/CLI, 
please update password and not use the default `changeme`

```
sudo scl enable rh-mariadb105 mysql

CREATE DATABASE misp;
CREATE USER misp@'localhost' IDENTIFIED BY 'changeme';
GRANT USAGE ON *.* to 'misp'@'localhost';
GRANT ALL PRIVILEGES on misp.* to 'misp'@'localhost';
FLUSH PRIVILEGES;
exit;
```

Load initial MISP schema (you'll be prompted for the password set above):

```
sudo scl enable rh-mariadb105 'mysql -u misp -p misp' < /var/www/MISP/INSTALL/MYSQL.sql
```

## MISP configuration

Setting up default bare configuration (please check MISP documentation for full
proper setup):

```
sudo cp -a /var/www/MISP/app/Config/core.default.php /var/www/MISP/app/Config/core.php
sudo cp -a /var/www/MISP/app/Config/bootstrap.default.php /var/www/MISP/app/Config/bootstrap.php
sudo cp -a /var/www/MISP/app/Config/config.default.php /var/www/MISP/app/Config/config.php
sudo cp -a /var/www/MISP/app/Config/database.default.php /var/www/MISP/app/Config/database.php
sudo chmod o-rwx /var/www/MISP/app/Config/{config.php,database.php,email.php}
sudo chown apache. /var/www/MISP/app/Config/{config.php,database.php,email.php}
```

Configure your database access (password `changeme` should be set accordingly
to the previous database setup phase):

`/var/www/MISP/app/Config/database.php`
```
<?php
class DATABASE_CONFIG {
  public $default = array(
    'datasource' => 'Database/Mysql',
    'persistent' => false,
    'host' => 'localhost',
    'login' => 'misp',
    'port' => 3306,
    'password' => 'changeme',
    'database' => 'misp',
    'prefix' => '',
    'encoding' => 'utf8',
  );
}
```

Adapt Python binary path in `/var/www/MISP/app/Config/config.php`

```
  'python_bin' => null,
```

should become (the path of the full Python Virtualenv shipped with RPMs):
```
  'python_bin' => '/var/www/cgi-bin/misp-virtualenv/bin/python',
```

## Install Redis server - rh-redis6-redis

```
sudo systemctl enable rh-redis6-redis
sudo systemctl start rh-redis6-redis
```

## Link php
```
ln -s /opt/rh/rh-php73/root/bin/php /usr/bin/php
```

## Enable and start misp-workers

```
sudo systemctl enable misp-workers
sudo systemctl start misp-workers
```

## Final extra setup items

- set owner and selinux context 
```bash
sudo chown apache:apache /var/www/MISP/app/Config/config.php
sudo chcon -t httpd_sys_rw_content_t /var/www/MISP/app/Config/config.php
```

Verify PHP extensions are properly enabled (should already be done through RPM
install)

- `/etc/opt/rh/rh-php73/php.d/redis.ini` 
  `extension=redis`
- `/etc/opt/rh/rh-php73/php.d/ssdeep.ini` 
  `extension=ssdeep`
- `/etc/opt/rh/rh-php73/php.d/brotli.ini` 
  `extension=brotli`
- `/etc/opt/rh/rh-php73/php.d/rdkafka.ini`
  `extension=rdkafka`

## Config firewalld for outside access

```bash
# open firewall for http and https
sudo firewall-cmd --permanent --zone=public --add-service http
sudo firewall-cmd --permanent --zone=public --add-service https
sudo systemctl restart firewalld
```

# Upgrade

Example upgrade procedure (always check upstream MISP documentation regarding
upgrades):

```
# stop main components
sudo systemctl stop httpd24-httpd misp-workers

# upgrade the MISP RPM package set
sudo rpm -U misp-*2.4.159*.rpm

# start everything
sudo systemctl start httpd24-httpd misp-workers

# first connection may take longer than usual if database schema migration have
# to be applied after upgrade
```
