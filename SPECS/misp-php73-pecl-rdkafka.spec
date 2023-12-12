%global php_inidir  %{_sysconfdir}/php.d
%global pecl_name   rdkafka
%global pecl_xmldir /var/lib/pear/pkgxml
%global php_extdir /opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules/

%define phprpm php73
%define _scl_php_loader /usr/bin/scl enable rh-%{phprpm}

Name:       misp-%{phprpm}-pecl-rdkafka
Version:    5.0.2
Release:    1%{?dist}
Summary:    PHP extension for interfacing rdkafka

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phprdkafka/phprdkafka/
Source0:    https://pecl.php.net/get/rdkafka-%{version}.tgz

BuildRequires:  rh-%{phprpm}-php, rh-%{phprpm}-php-devel, rh-%{phprpm}-php-pear 
BuildRequires: 	rh-%{phprpm}-php-cli
BuildRequires:	librdkafka librdkafka-devel
Requires:       rh-%{phprpm}-php

%description
PHP extension for interfacing rdkafka

%prep
%setup -q -n rdkafka-%{version}

# create the ini file
cat > %{pecl_name}.ini << EOF
extension=%{pecl_name}.so
EOF

%build
/opt/rh/rh-%{phprpm}/root/bin/phpize
%configure \
    --enable-rdkafka \
    --with-php-config=/opt/rh/rh-%{phprpm}/root/bin/php-config
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}/etc/opt/rh/rh-%{phprpm}/php.d/%{pecl_name}.ini

%files
%{php_extdir}/%{pecl_name}.so
%config(noreplace) /etc/opt/rh/rh-%{phprpm}/php.d/%{pecl_name}.ini

%changelog
* Mon Nov 20 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 5.3.7
- first version for rh-php73
