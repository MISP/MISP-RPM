%global php_inidir  %{_sysconfdir}/php.d
%global pear_name  Console_CommandLine

Name:       misp-php82-pear-command-line
Version:    1.2.2
Release:    1%{?dist}
Summary:    A full featured command line options and arguments parser

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpcrypt-gpg/phpcrypt-gpg/
Source0:    http://download.pear.php.net/get/%{pear_name}-%{version}.tgz

BuildArch:	noarch

BuildRequires:  php, php-devel
BuildRequires:	php-cli, php-pear
Requires:       php, php-pear

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
pear -d php_dir=/usr/share/pear install --nodeps --packagingroot $RPM_BUILD_ROOT %{pear_name}-%{version}.tgz

%files
/usr/share/pear/Console/CommandLine/*
/usr/share/pear/Console/CommandLine*php
/usr/share/pear-data/Console_CommandLine/*
/usr/share/tests/pear/Console_CommandLine/*
%doc /usr/share/doc/pear/Console_CommandLine
/var/lib/pear/.registry/console_commandline.reg
%exclude /var/lib/pear/.channels
%exclude /var/lib/pear/.filemap
%exclude /var/lib/pear/.lock

%changelog
* Fri Dec 20 2024 Andreas Muehlemann <amuehlem@gmail.com> - 1.2.2
- first version for RHEL8
