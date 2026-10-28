%global php_inidir  %{_sysconfdir}/php.d
%global pear_name   Crypt_GPG

Name:       misp-php-pear-crypt-gpg
Version:    1.6.11
Release:    1%{?dist}
Summary:    PHP extension for interfacing crypt-gpg

Obsoletes:	misp-php82-pear-crypt-gpg  < 1.6.11
Conflicts:  misp-php82-pear-crypt-gpg  < 1.6.11

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpcrypt-gpg/phpcrypt-gpg/
Source0:    http://download.pear.php.net/get/%{pear_name}-%{version}.tgz

BuildArch:	noarch

BuildRequires:  php, php-devel
BuildRequires:	php-cli, php-pear(PEAR)
Requires:       php, php-pear(PEAR)

%description
PHP extension for interfacing crypt-gpg

%prep
%setup -q -c
cd %{pear_name}-%{version}

%build
cd %{pear_name}-%{version}

%install
cd %{pear_name}-%{version}
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
* Wed Oct 28 2026 Andreas Muehlemann <amuehlem@gmail.com> - 1.6.11
- update to 1.6.11
