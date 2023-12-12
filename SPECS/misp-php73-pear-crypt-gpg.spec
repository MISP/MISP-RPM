%global php_inidir  %{_sysconfdir}/php.d
%global pear_name   Crypt_GPG

%define phprpm php73
%define _scl_php_loader /usr/bin/scl enable rh-%{phprpm}

Name:       misp-%{phprpm}-pear-crypt-gpg
Version:    1.6.7
Release:    1%{?dist}
Summary:    PHP extension for interfacing crypt-gpg

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpcrypt-gpg/phpcrypt-gpg/
Source0:    http://download.pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRequires:  rh-%{phprpm}-php, rh-%{phprpm}-php-devel, rh-%{phprpm}-php-pear 
BuildRequires: 	rh-%{phprpm}-php-cli
Requires:       rh-%{phprpm}-php, rh-%{phprpm}-php-pear

%description
PHP extension for interfacing crypt-gpg

%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{pear_name}.xml

%build
cd %{pear_name}-%{version}

%install
/opt/rh/rh-%{phprpm}/root/bin/pear -d php_dir=/tmp install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}-%{version}.tgz
cp -r $RPM_BUILD_ROOT/tmp/Crypt $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/share/pear
cp -r /tmp/.registry $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/share/pear


%files
/opt/rh/rh-%{phprpm}/root/usr/share/pear/GPG/*
/opt/rh/rh-%{phprpm}/root/usr/share/pear/GPG*php
/opt/rh/rh-%{phprpm}/root/usr/share/pear-data/Crypt_GPG/*
/opt/rh/rh-%{phprpm}/root/usr/share/tests/pear/Crypt_GPG/*
/opt/rh/rh-%{phprpm}/root/usr/bin/crypt-gpg-pinentry
%doc /opt/rh/rh-%{phprpm}/root/usr/share/doc/pear/Crypt_GPG/*
/opt/rh/rh-%{phprpm}/root/var/lib/pear/.registry/crypt_gpg.reg
%exclude /opt/rh/rh-%{phprpm}/root/var/lib/pear/.channels
%exclude /opt/rh/rh-%{phprpm}/root/var/lib/pear/.filemap
%exclude /opt/rh/rh-%{phprpm}/root/var/lib/pear/.lock
%exclude /tmp/Crypt

%changelog
* Mon Nov 20 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 5.3.7
- first version for rh-php73
