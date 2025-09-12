%global __python %{__python3}
%global _python_bytecompile_extra 0
%global debug_package %{nil}
%define _build_id_links none
%define _binaries_in_noarch_packages_terminate_build 0
# disable mangling of shebangs #!
%define __brp_mangle_shebangs /usr/bin/true
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

# exclude for requirements
%global __requires_exclude ^/opt/python/cp3.*

# global definitions
%define pymispver 2.5.17
%define mispstixver 2025.8.4

# RHEL version dependencies
%define phpver 83
%define pythonvershort python3.12
%define pythonver python3.12
%define pythonbin python3.12

%if 0%{?rhel} == 8
%define phpver 82
%define pythonver python3.12
%define pythonvershort python3.12
%define pythonbin python3.12
%endif
%if 0%{?rhel} == 9
%define phpver 82
%define pythonver python3.12
%define pythonvershort python3.12
%define pythonbin python3.12
%endif
%if 0%{?rhel} == 10
%define pythonver python3.12
%define pythonvershort python3
%define pythonbin python3
%endif

Name:		misp
Version:	2.5.21
Release: 	1%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source1:	misp.conf
Source2:        misp-httpd.pp
Source3:        misp-bash.pp
Source4:        misp-ps.pp
Source5:        misp-workers.service
Source6:        start-misp-workers.sh
Source7:        misp-workers.ini
Source8:        misp-workers8.pp
Source9:        misp-worker-status-supervisord.pp
Patch0:         MISP-AppModel.php.patch
Patch1:         misp-2.4.177-fix-composer-config.patch

BuildRequires:	git, %{pythonvershort}-devel, %{pythonvershort}-pip
BuildRequires:	libxslt-devel, zlib-devel
BuildRequires:	bash-completion
BuildRequires:  php, php-cli, php-xml
BuildRequires:  php-mbstring, php-json
BuildRequires:  ssdeep-libs, ssdeep-devel
BuildRequires:  cmake3, bash-completion
BuildRequires:  wget

%if 0%{?rhel} < 9
BuildRequires:  /usr/bin/pathfix.py
%endif

Requires:       httpd, mod_ssl, libxslt, zlib
Requires:       mariadb, mariadb-server
Requires:	(php or php-fpm)
Requires:       php-cli, php-gd, php-pdo
Requires:       php-mysqlnd, php-mbstring, php-xml
Requires:       php-bcmath, php-opcache, php-json
Requires:       php-pecl-zip, php-intl
Requires:       misp-php-pecl-ssdeep, php-process
Requires:       php-pecl-apcu, misp-php-pecl-brotli, misp-php-pecl-rdkafka
Requires:       misp-php-pear-crypt-gpg, misp-php-pear-command-line

# redis / valkey depending on rhel version
%if 0%{?rhel} < 10
Requires:  redis
%endif
%if 0%{?rhel} > 9
Requires:  valkey
%endif

%package python-virtualenv
Summary: 	the python virtual environment for MISP
Group:		Internet Applications
License:	GPLv3

%description python-virtualenv
The python vitualenvironment for MISP

%description
MISP - malware information sharing platform & threat sharing

%prep
%setup -q -T -c

git clone https://github.com/MISP/MISP.git
cd MISP
git checkout v%{version}
git submodule update --init --recursive
git submodule foreach --recursive git config core.filemode false
git config core.filemode false

# patch app/Model/Server.php to show commit ID
patch --ignore-whitespace -p0 < %{PATCH0}

# patch app/composer.json
patch --ignore-whitespace -p0 < %{PATCH1}

%build
#intentionally left blank

%install
mkdir -p $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/app $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/PyMISP $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/format $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/tools $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/*.json $RPM_BUILD_ROOT/var/www/MISP
cp -r MISP/.git $RPM_BUILD_ROOT/var/www/MISP
mkdir -p $RPM_BUILD_ROOT/var/www/MISP/INSTALL
cp MISP/INSTALL/*.sql $RPM_BUILD_ROOT/var/www/MISP/INSTALL

# create initial configuartion files
cd $RPM_BUILD_ROOT/var/www/MISP/app/Config
cp bootstrap.default.php bootstrap.php
cp config.default.php config.php
cp core.default.php core.php
cp database.default.php database.php

# create python3 virtualenv
%{pythonbin} -m venv --copies $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv

$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U pip setuptools

$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install ordered-set python-dateutil six weakrefmethod
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/misp-stix

cd $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/python-cybox
git config core.filemode false
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install .

cd $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/python-stix
git config core.filemode false
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install .

cd $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/mixbox
git config core.filemode false
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install .

cd $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/cti-python-stix2
git config core.filemode false
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install .

cd $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/python-maec
git config core.filemode false
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install .

$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U zmq
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U redis
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U python-magic
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U plyara
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U pydeep
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U lief

cd $RPM_BUILD_ROOT/var/www/MISP/PyMISP
$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U .

# CakePHP
cd $RPM_BUILD_ROOT/var/www/MISP/app
/usr/bin/php composer.phar install --no-dev
/usr/bin/php composer.phar require --with-all-dependencies supervisorphp/supervisor:^4.0 guzzlehttp/guzzle php-http/message php-http/message-factory lstrojny/fxmlrpc jakub-onderka/openid-connect-php

cd $RPM_BUILD_ROOT/var/www/MISP

# clean up before PATH rewriting
rm -rf $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/pyvenv.cfg
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -e "s|%{buildroot}||g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/lib/%{pythonver}/site-packages/*/direct_url.json

# path fix for python3 for RHEL8
%if 0%{?rhel} < 9
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT/var/www/MISP/*
%endif

%py3_shebang_fix $RPM_BUILD_ROOT/var/www/MISP

# save commit ID of this installation
git rev-parse HEAD > .git_commit_version

# cleanup
pushd $RPM_BUILD_ROOT
find . -not -name '.git_commit_version' -name .git* | xargs rm -rf
find . -type f -name empty | xargs rm -f

rm -f var/www/MISP/app/Makefile
rm -f var/www/MISP/app/update_thirdparty.sh
popd

mkdir -p $RPM_BUILD_ROOT/etc/httpd/conf.d
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/etc/httpd/conf.d/
mkdir -p $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE8} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE9} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
mkdir -p $RPM_BUILD_ROOT/usr/local/sbin
install -m 755 %{SOURCE6} $RPM_BUILD_ROOT/usr/local/sbin
chmod g+w $RPM_BUILD_ROOT/var/www/MISP/app/Config
mkdir -p $RPM_BUILD_ROOT/etc/supervisord.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/etc/supervisord.d

%files python-virtualenv
%defattr(-,apache,apache,-)
/var/www/cgi-bin/misp-virtualenv
%exclude /var/www/cgi-bin/misp-virtualenv/*.pyc

%files
%defattr(-,apache,apache,-)
%doc MISP/{AUTHORS,CITATION.cff,code_of_conduct.md,CODINGSTYLE.md,CONTRIBUTING.md,GITWORKFLOW.md,README.md,ROADMAP.md,SECURITY.md}
%doc MISP/docs
%license MISP/LICENSE
/var/www/MISP
# configuration directory: read or read/write permission, through group ownership
%dir %attr(0775,root,apache) /var/www/MISP/app/Config
%config(noreplace) %attr(0640,root,apache) /var/www/MISP/app/Config/bootstrap.php
%config(noreplace) %attr(0660,root,apache) /var/www/MISP/app/Config/config.php
%config(noreplace) %attr(0640,root,apache) /var/www/MISP/app/Config/core.php
%config(noreplace) %attr(0640,root,apache) /var/www/MISP/app/Config/database.php
%config(noreplace) %attr(0640,root,apache) /var/www/MISP/app/Config/email.php
%config(noreplace) %attr(0640,root,apache) /var/www/MISP/app/Config/routes.php
%config(noreplace) /var/www/MISP/app/Plugin/CakeResque/Config/config.php
# data directories: full read/write access, through user ownership
%attr(-,apache,apache) /var/www/MISP/app/tmp
%attr(-,apache,apache) /var/www/MISP/app/files
%attr(-,apache,apache) /var/www/MISP/app/Plugin/CakeResque/tmp
%config(noreplace) /etc/httpd/conf.d/misp.conf
%config(noreplace) /etc/supervisord.d/misp-workers.ini
/usr/share/MISP/policy/selinux/misp-*.pp
%{_sysconfdir}/systemd/system/misp-workers.service
/usr/local/sbin/start-misp-workers.sh
# exclude test files whicht get detected by AV solutions
%exclude /var/www/MISP/PyMISP/tests
%exclude /var/www/MISP/*.pyc

%post
SELINUXSTATUS=$(getenforce);
if [ SELINUXSTATUS != 'Disabled' ]; then
    chcon -t httpd_sys_rw_content_t /var/www/MISP/app/files
    chcon -t httpd_sys_rw_content_t /var/www/MISP/app/files/terms
    chcon -t httpd_sys_rw_content_t /var/www/MISP/app/files/scripts/tmp
    chcon -t httpd_sys_rw_content_t /var/www/MISP/app/Plugin/CakeResque/tmp
    chcon -R -t httpd_sys_rw_content_t /var/www/MISP/app/tmp
    chcon -R -t httpd_sys_rw_content_t /var/www/MISP/app/webroot/img/orgs
    chcon -R -t httpd_sys_rw_content_t /var/www/MISP/app/webroot/img/custom
    setsebool -P httpd_can_network_connect 1
    setsebool -P httpd_unified 1
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/'
    restorecon -v '/var/www/MISP/app/tmp/'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/logs/'
    restorecon -v '/var/www/MISP/app/tmp/logs/'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/'
    restorecon -v '/var/www/MISP/app/tmp/cache/'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/feeds'
    restorecon -v '/var/www/MISP/app/tmp/cache/feeds'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/models'
    restorecon -v '/var/www/MISP/app/tmp/cache/models'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/persistent'
    restorecon -v '/var/www/MISP/app/tmp/cache/persistent'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/tmp/cache/views'
    restorecon -v '/var/www/MISP/app/tmp/cache/views'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/Config/config.php'
    restorecon -v '/var/www/MISP/app/Config/config.php'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/Lib/cakephp/lib/Cake/Config/config.php'
    restorecon -v '/var/www/MISP/app/Lib/cakephp/lib/Cake/Config/config.php'
    semanage fcontext -a -t httpd_sys_rw_content_t '/var/www/MISP/app/Plugin/CakeResque/Config/config.default.php'
    restorecon -v '/var/www/MISP/app/Plugin/CakeResque/Config/config.php'
    semodule -i /usr/share/MISP/policy/selinux/misp-httpd.pp
    semodule -i /usr/share/MISP/policy/selinux/misp-bash.pp
    semodule -i /usr/share/MISP/policy/selinux/misp-ps.pp
    semodule -i /usr/share/MISP/policy/selinux/misp-workers8.pp
    semodule -i /usr/share/MISP/policy/selinux/misp-worker-status-supervisord.pp
fi

%changelog
* Thu Sep 11 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.21
- update to 2.5.21

* Sat Aug 30 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.20
- update to 2.5.20
- remove php version dependecies in required packages

* Fri Aug 29 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.19
- update to 2.5.19
- sync to misp25.spec from amuehlem/MISP-RPM
- update to use python3.12

* Sat Aug 9 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.18
- update to 2.5.18

* Tue Aug 5 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.17
- update to 2.5.17

* Tue Jul 15 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.16
- update to 2.5.16

* Sun Jun 22 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.15
- update to 2.5.15

* Thu Jun 19 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.14
- update to 2.5.14
- adding jakub-onderka/openid-connect-php php dependency

* Fri Jun 13 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.13
- update to 2.5.13

* Wed May 14 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.12
- update to 2.5.12

* Mon May 12 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.11
- update to 2.5.11

* Wed Apr 9 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.10
- update to 2.5.10

* Mon Feb 24 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.7
- update to 2.5.7

* Thu Feb 6 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.6
- update to 2.5.2
- update to 2.5.3
- update to 2.5.4
- update to 2.5.5
- update to 2.5.6

* Wed Feb 5 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.5.1
- first version for RHEL9-pure (no EPEL or REMI PHP repo)
- update to 2.5.1
