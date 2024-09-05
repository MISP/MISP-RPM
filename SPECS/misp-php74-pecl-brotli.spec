%global php_inidir  %{_sysconfdir}/php.d
%global pecl_name   brotli
%global pecl_xmldir /var/lib/pear/pkgxml
%global php_extdir /usr/lib64/php/modules/

Name:       misp-php74-pecl-brotli
Version:    0.14.2
Release:    1%{?dist}
Summary:    PHP extension for interfacing brotli

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpbrotli/phpbrotli/
Source0:    https://pecl.php.net/get/brotli-%{version}.tgz

BuildRequires:  php >= 7.4, php < 8, php-devel >= 7.4, php-devel < 8
BuildRequires: 	php-cli >= 7.4, php-cli < 8
BuildRequires:	php-pear
BuildRequires:	brotli, brotli-devel
Requires:       php

%description
PHP extension for interfacing brotli

%prep
%setup -q -n brotli-%{version}

# create the ini file
cat > %{pecl_name}.ini << EOF
extension=%{pecl_name}.so
EOF

%build
# brotli hard codes /usr/lib for libfuzzy.so
phpize
./configure \
    --with-brotli \
    --with-php-config=/usr/bin/php-config
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}/etc/php.d/%{pecl_name}.ini

%files
%{php_extdir}/%{pecl_name}.so
%config(noreplace) /etc/php.d/%{pecl_name}.ini

%changelog
* Thu Sep 5 2024 Andreas Muehlemann <amuehlem@gmail.com> - 5.3.7
- first version for rh-php74
