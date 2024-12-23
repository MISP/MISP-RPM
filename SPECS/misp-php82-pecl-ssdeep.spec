%global php_inidir  %{_sysconfdir}/php.d
%global pecl_name   ssdeep
%global pecl_xmldir /var/lib/pear/pkgxml
%global php_extdir /usr/lib64/php/modules/

Name:       misp-php82-pecl-ssdeep
Version:    1.1.0
Release:    1%{?dist}
Summary:    PHP extension for interfacing ssdeep

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpssdeep/phpssdeep/
Source0:    https://pecl.php.net/get/ssdeep-%{version}.tgz

Patch0:	    https://patch-diff.githubusercontent.com/raw/php/pecl-text-ssdeep/pull/2.patch

BuildRequires:  php, php-devel
BuildRequires: 	php-cli, php-pear
BuildRequires:	ssdeep, ssdeep-devel, patch
Requires:       php

%description
PHP extension for interfacing ssdeep

%prep
%setup -q -n ssdeep-%{version}

# create the ini file
cat > %{pecl_name}.ini << EOF
extension=%{pecl_name}.so
EOF

%build
# patch for php8
patch -p1 < %{PATCH0}

# ssdeep hard codes /usr/lib for libfuzzy.so
phpize
./configure \
    --with-ssdeep=%{_libdir} \
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
- first version for php74
