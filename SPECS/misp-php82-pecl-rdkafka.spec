%global php_inidir  %{_sysconfdir}/php.d
%global pecl_name   rdkafka
%global pecl_xmldir /var/lib/pear/pkgxml
%global php_extdir /usr/lib64/php/modules/

Name:       misp-php82-pecl-rdkafka
Version:    5.0.2
Release:    1%{?dist}
Summary:    PHP extension for interfacing rdkafka

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phprdkafka/phprdkafka/
Source0:    https://pecl.php.net/get/rdkafka-%{version}.tgz

BuildRequires:  php, php-devel
BuildRequires: 	php-cli, php-pear
BuildRequires:	librdkafka librdkafka-devel
Requires:       php

%description
PHP extension for interfacing rdkafka

%prep
%setup -q -n rdkafka-%{version}

# create the ini file
cat > %{pecl_name}.ini << EOF
extension=%{pecl_name}.so
EOF

%build
phpize
%configure \
    --enable-rdkafka \
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
- first version for rh-php74
