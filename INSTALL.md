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
sudo yum install -y scl-utils ca-certificates
```

## Install Apache webserver - httpd24

```bash
sudo yum install -y httpd24 httpd24-mod_ssl
sudo systemctl enable httpd24-httpd
sudo systemctl restart httpd24-httpd
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
rpm -i faup-1.6+*.rpm
rpm -i gtcaca-1.0+*.rpm

# prereq PHP extensions for misp
export mispver="2.4.158-1"
rpm -i misp-pear-crypt-gpg-$mispver.el7.x86_64.rpm
rpm -i misp-pecl-rdkafka-$mispver.el7.x86_64.rpm
rpm -i misp-pecl-redis-$mispver.el7.x86_64.rpm
rpm -i misp-pecl-ssdeep-$mispver.el7.x86_64.rpm
rpm -i misp-php-brotli-$mispver.el7.x86_64.rpm
rpm -i misp-python-virtualenv-$mispver.el7.x86_64.rpm

# install misp rpm
rpm -i misp-$mispver.el7.x86_64.rpm
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
sudo yum install -y rh-mariadb105-mariadb rh-mariadb105-mariadb-server-utils
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
sudo cp -a app/Config/core.default.php app/Config/core.php
sudo cp -a app/Config/bootstrap.default.php app/Config/bootstrap.php
sudo cp -a app/Config/config.default.php app/Config/config.php
sudo chmod o-rwx app/Config/{config.php,database.php,email.php}
```

Configure your database access (password `changeme` should be set accordingly
to the previous database setup phase):

`/var/www/MISP/app/Config/database.php`
```
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
  'python_bin' => NULL,
```

should become (the path of the full Python Virtualenv shipped with RPMs):
```
  'python_bin' => '/var/www/cgi-bin/misp-virtualenv/bin/python',
```

## Install Redis server - rh-redis6-redis

```
sudo yum install -y rh-redis6-redis
sudo systemctl enable rh-redis6-redis
sudo systemctl start rh-redis6-redis
```

## Enable and start misp-workers

```
sudo systemctl enable misp-workers
sudo systemctl start misp-workers
```

Note - the Systemd Unit should make use of the software collection with the
`scl` wrapper.

`/etc/systemd/system/misp-workers.service` should have a line similar to

```
ExecStart=/usr/bin/scl enable rh-php73 /var/www/MISP/app/Console/worker/start.sh
```

## Final extra setup items

- set owner and selinux context 
```bash
sudo chown apache:apache /var/www/MISP/app/Config/config.php
sudo chcon -t httpd_sys_rw_content_t /var/www/MISP/app/Config/config.php
```

Verify PHP extensions are properly enabled (should already be done through RPM
install)

- `/etc/opt/rh/rh-php73/php.d/40-redis.ini` 
  `extension=redis`
- `/etc/opt/rh/rh-php73/php.d/40-ssdeep.ini` 
  `extension=ssdeep`
- `/etc/opt/rh/rh-php73/php.d/40-brotli.ini` 
  `extension=brotli`
- `/etc/opt/rh/rh-php73/php.d/40-rdkafka.ini`
  `extension=rdkafka`

## Config firewalld for outside access

```bash
# open firewall for http and https
firewall-cmd --permanent --zone=public --add-service http
firewall-cmd --permanent --zone=public --add-service https
systemctl restart firewalld
```

# MISP startup
# initial password
oi5pai6naPhedaefohghahghu3Vaeth9ihohtoGev4oosooz0xeiZ9shoh0ahthah6iepae5Quiw6thiuS2xah0ohp9ohrooch8igheakiiCeiwai3ohdeew9phiesho8caedeighea6baewei3eekuichaip6cie9sugh9Hei3aih9caeje8Ohm9ikuuhua7ooVie9YohmailahNak5uZah8ew3iivohCaoshee1vieB7eirahdeedei1Veyah9


# Upgrade

Example upgrade procedure (always check upstream MISP documentation regarding
upgrades):

```
# stop main components
sudo systemctl stop httpd24-httpd misp-workers

# upgrade the MISP RPM package set
sudo rpm -U misp-*2.4.158*.rpm

# start everything
sudo systemctl start httpd24-httpd misp-workers

# first connection may take longer than usual if database schema migration have
# to be applied after upgrade
```
