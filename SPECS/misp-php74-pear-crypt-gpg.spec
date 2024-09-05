%global php_inidir  %{_sysconfdir}/php.d
%global pear_name   Crypt_GPG

Name:       misp-php74-pear-crypt-gpg
Version:    1.6.7
Release:    1%{?dist}
Summary:    PHP extension for interfacing crypt-gpg

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpcrypt-gpg/phpcrypt-gpg/
Source0:    http://download.pear.php.net/get/%{pear_name}-%{version}.tgz

BuildArch:	noarch

BuildRequires:  php >= 7.4, php < 8, php-devel >= 7.4 , php-devel < 8
BuildRequires:	php-cli >= 7.4, php-cli < 8
BuildRequires: 	php-pear
Requires:       php >= 7.4, php < 8, php-pear

%description
PHP extension for interfacing crypt-gpg

%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{pear_name}.xml

%build
cd %{pear_name}-%{version}

%install
pear -d php_dir=/usr/share/pear install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}-%{version}.tgz

%files
/usr/share/pear/Crypt/GPG/*
/usr/share/pear/Crypt/GPG*php
/usr/share/pear-data/Crypt_GPG/*
/usr/share/tests/pear/Crypt_GPG/*
/usr/bin/crypt-gpg-pinentry
%doc /usr/share/doc/pear/Crypt_GPG/*
/var/lib/pear/.registry/crypt_gpg.reg
%exclude /var/lib/pear/.channels
%exclude /var/lib/pear/.filemap
%exclude /var/lib/pear/.lock
%exclude /tmp/Crypt

%changelog
* Thu Sep 5 2024 Andreas Muehlemann <amuehlem@gmail.com> - 5.3.7
- first version for rh-php74
