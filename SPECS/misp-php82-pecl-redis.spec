%global php_inidir  %{_sysconfdir}/php.d
%global pecl_name   redis
%global pecl_xmldir /var/lib/pear/pkgxml
%global php_extdir /usr/lib64/php/modules/

Name:       misp-php82-pecl-redis
Version:    5.3.7
Release:    1%{?dist}
Summary:    PHP extension for interfacing redis

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpredis/phpredis/
Source0:    https://pecl.php.net/get/redis-%{version}.tgz

BuildRequires:  php, php-devel
BuildRequires: 	php-cli, php-pear
Requires:       php

%description
PHP extension for interfacing redis

%prep
%setup -q -n redis-%{version}

# create the ini file
cat > %{pecl_name}.ini << EOF
extension=%{pecl_name}.so
EOF

%build
phpize
%configure \
    --enable-redis \
    --enable-redis-session \
    --with-php-config=/usr/bin/php-config
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}/etc/php.d/%{pecl_name}.ini

%files
%{php_extdir}/%{pecl_name}.so
%config(noreplace) /etc/php.d/%{pecl_name}.ini

%changelog
* Tue Feb 4 2025 Andreas Muehlemann <amuehlem@gmail.com> - 5.3.7
- first version for rhel8
