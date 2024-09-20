# MISP-RPM installation for RHEL8

This document is specifically written for RHEL 8.x installation with not external repositories as the epel repository or remi repo for PHP packages. Please follow the MISP upstream official documentation for anything MISP related.

The main differences with a regular MISP installed are around RHEL software collection specifics and packaging.

To start, you need a valid RHEL subscription and minimal system installed.

## enable necessary RHEL repos
The rhel-8-for-x86_64-baseos-rpms should be enabled by default. To check which repositories are already configured just use the following command

```
subscription-manager repos --list-enabled
```

The following repos must be activated to proceed with the installation

```
subscription-manager repos --enable=rhel-8-for-x86_64-baseos-rpms
subscription-manager repos --enable=rhel-8-for-x86_64-appstream-rpms
subscription-manager repos --enable=codeready-builder-for-rhel-8-x86_64-rpms
```

## enable specific software modules

```
dnf module enable php:7.4
dnf module enable mariadb:10.11
```

## install provided RPMs

```
# prereq for misp
sudo yum install -y gtcaca-*.rpm libcaca*.rpm imlib2*.rpm
sudo yum install -y faup-*.rpm
sudo yum install -y ssdeep-libs*.rpm
sudo yum install -y libbrotli*.rpm
sudo yum install -y misp-php74-*rpm

# install misp rpm
sudo yum install -y misp-python-virtualenv-2.4.*.rpm misp-2.4.*.rpm
```

## Adjust PHP settings
All PHP related settings are in ```/etc/php.ini```

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

## MISP configuration
Setting up default bare configuration (please check MISP documentation for full proper setup):

```
# set DB details in database.php
# set baseurl in config.php
# set python_bin => '/var/www/cgi-bin/misp-virtualenv/bin/python3'

sudo chown apache:apache /var/www/MISP/app/Config/config.php
sudo chcon -t httpd_sys_rw_content_t /var/www/MISP/app/Config/config.php
```

## Install MariaDB database

It's recommended to secure mariadb with the provided script

```
mysql_secure_installation
```

Now you can create the MISP database
```
CREATE DATABASE misp;
CREATE USER misp@'localhost' IDENTIFIED BY 'changeme';
GRANT USAGE ON *.* to 'misp'@'localhost';
GRANT ALL PRIVILEGES on misp.* to 'misp'@'localhost';
FLUSH PRIVILEGES;
exit;
```

Install the base database schema

```
mysql -u misp -p misp < /var/www/MISP/INSTALL/MYSQL.sql
```

## enable services

```
systemctl enable mariadb
systemctl start mariadb
systemctl enable redis
systemctl start redis
systemctl enable php-fpm
systemctl start php-fpm
systemctl enable httpd
systemctl start httpd
systemctl enable misp-workers
systemctl start misp-workers
```

## open firewall for access on http and https

```
firewall-cmd --permanent --zone=public --add-service http
firewall-cmd --permanent --zone=public --add-service https
systemctl restart firewalld
```

reboot to make sure all services are started correctly
