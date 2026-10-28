%global php_inidir  %{_sysconfdir}/php.d
%global pecl_name   redis
%global pecl_xmldir /var/lib/pear/pkgxml
%global php_extdir /usr/lib64/php/modules/

Name:       misp-php-redis
Version:    6.3.0
Release:    1%{?dist}
Summary:    PHP extension for interfacing redis

Obsoletes:	misp-php82-pecl-redis = 5.3.7

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpredis/phpredis/

BuildRequires:  git
BuildRequires:  php, php-devel
BuildRequires: 	php-cli, php-pear
Requires:       php

%description
PHP extension for interfacing redis

%prep
%setup -qTc
git clone https://github.com/phpredis/phpredis.git

%build
cd phpredis
phpize
%configure \
    --enable-redis \
    --enable-redis-session \
    --with-php-config=/usr/bin/php-config \
    --with-libdir=%{_lib}

make %{?_smp_mflags}

# create the ini file
cat > %{pecl_name}.ini << EOF
extension=%{pecl_name}.so
EOF

%install
cd phpredis
make install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}/etc/php.d/%{pecl_name}.ini

%files
%{php_extdir}/%{pecl_name}.so
%config(noreplace) /etc/php.d/%{pecl_name}.ini

%changelog
* Wed Oct 28 2026 Andreas Muehlemann <amuehlem@gmail.com> - 6.3.0
- renaming the package
- update to 6.3.0

