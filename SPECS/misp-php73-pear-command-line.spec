%global php_inidir  %{_sysconfdir}/php.d
%global pear_name  Console_CommandLine

%define phprpm php73
%define _scl_php_loader /usr/bin/scl enable rh-%{phprpm}

Name:       misp-%{phprpm}-pear-command-line
Version:    1.2.2
Release:    1%{?dist}
Summary:    A full featured command line options and arguments parser

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpcrypt-gpg/phpcrypt-gpg/
Source0:    http://download.pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRequires:  rh-%{phprpm}-php, rh-%{phprpm}-php-devel, rh-%{phprpm}-php-pear 
BuildRequires: 	rh-%{phprpm}-php-cli
Requires:       rh-%{phprpm}-php, rh-%{phprpm}-php-pear

%description
Console_CommandLine is a full featured package for managing command-line
options and arguments highly inspired from python optparse module, it allows
the developer to easily build complex command line interfaces.

Main features:
* handles sub commands (ie. $ myscript.php -q subcommand -f file),
* can be completely built from an xml definition file,
* generate --help and --version options automatically,
* can be completely customized,
* builtin support for i18n,
* and much more...

%prep
%setup -q -c
cd %{pear_name}-%{version}
mv ../package.xml %{pear_name}.xml

%build
cd %{pear_name}-%{version}

%install
/opt/rh/rh-%{phprpm}/root/bin/pear -d php_dir=/tmp install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}-%{version}.tgz
cp -r $RPM_BUILD_ROOT/tmp/Console $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/share/pear

%files
/opt/rh/rh-%{phprpm}/root/usr/share/pear/CommandLine/*
/opt/rh/rh-%{phprpm}/root/usr/share/pear/CommandLine*php
/opt/rh/rh-%{phprpm}/root/usr/share/pear-data/Console_CommandLine/*
/opt/rh/rh-%{phprpm}/root/usr/share/tests/pear/Console_CommandLine/*
%doc /opt/rh/rh-%{phprpm}/root/usr/share/doc/pear/Console_CommandLine
/opt/rh/rh-%{phprpm}/root/var/lib/pear/.registry/console_commandline.reg
%exclude /opt/rh/rh-%{phprpm}/root/var/lib/pear/.channels
%exclude /opt/rh/rh-%{phprpm}/root/var/lib/pear/.filemap
%exclude /opt/rh/rh-%{phprpm}/root/var/lib/pear/.lock
%exclude /tmp

%changelog
* Mon Nov 20 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 5.3.7
- first version for rh-php73
