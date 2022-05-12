%global __python %{__python3}
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global _python_bytecompile_extra 0
%define _binaries_in_noarch_packages_terminate_build 0
# disable mangling of shebangs #!
%define __brp_mangle_shebangs /usr/bin/true

%define mispver 2.4.155
%define phprpm php73
%define pyrpm python38
%define phpbrotliver 0.13.1

Name:		misp
Version:	%{mispver}
Release: 	4%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source1:        misp-httpd.pp
Source2:        misp-bash.pp
Source3:        misp-ps.pp
Source4:        misp-workers.service

#BuildRequires:	/usr/bin/pathfix.py
BuildRequires:	git, rh-%{pyrpm}-python-devel, rh-%{pyrpm}-python-pip, libxslt-devel, zlib-devel
BuildRequires:	rh-%{phprpm}-php, rh-%{phprpm}-php-cli, rh-%{phprpm}-php-xml, rh-%{phprpm}-php-mbstring
BuildRequires:  rh-%{phprpm}-php-pear, rh-%{phprpm}-php-devel
BuildRequires:  ssdeep-libs, ssdeep-devel
BuildRequires:  librdkafka librdkafka-devel
BuildRequires:	cmake3, bash-completion
BuildRequires:	libcaca-devel

Requires:	httpd24, httpd24-mod_ssl, rh-redis6-redis, libxslt, zlib
Requires:	rh-mariadb105-mariadb
Requires:	rh-%{pyrpm}-python, misp-python-virtualenv
Requires:	rh-%{phprpm}-php, rh-%{phprpm}-php-cli, rh-%{phprpm}-php-gd, rh-%{phprpm}-php-pdo
Requires:	rh-%{phprpm}-php-mysqlnd, rh-%{phprpm}-php-mbstring, rh-%{phprpm}-php-xml
Requires:       rh-%{phprpm}-php-bcmath, rh-%{phprpm}-php-opcache, rh-%{phprpm}-php-json
Requires:       rh-%{phprpm}-php-zip, misp-pecl-redis, rh-php73-php-intl
Requires:       misp-pear-crypt-gpg, misp-pecl-ssdeep, ssdeep-libs
Requires:	misp-php-brotli, misp-pecl-rdkafka
Requires:	gtcaca faup

%package python-virtualenv
Summary:        the python virtual environment for MISP
Group:          Internet Applications
License:        GPLv3

%description python-virtualenv
The python vitualenvironment for MISP

%package pecl-redis
Summary:        PECL redis extension
Group:          Internet Applications
License:        GPLv3

%description pecl-redis
The PECL redis extension

%package pecl-ssdeep
Summary:        PECL ssdeep extension
Group:          Internet Applications
License:        GPLv3

%description pecl-ssdeep
The PECL ssdeep extension

%package pear-crypt-gpg
Summary:        PEAR Crypt_GPG extension
Group:          Internet Applications
License:        GPLv3

%description pear-crypt-gpg
The PEAR redis extension

%package php-brotli
Summary:        Brotli upstream PHP extension
Group:          Internet Applications
License:        GPLv3

%description php-brotli
Brotli upstream PHP extension

%package pecl-rdkafka
Summary:        PECL rdkafka extension
Group:          Internet Applications
License:        GPLv3

%description pecl-rdkafka
The PECL rdkafka extension

%description
MISP - malware information sharing platform
The MISP threat sharing platform is a free and open source software 
helping information sharing of threat intelligence including cyber 
security indicators.

A threat intelligence platform for gathering, sharing, storing and 
correlating Indicators of Compromise of targeted attacks, threat 
intelligence, financial fraud information, vulnerability information or 
even counter-terrorism information. 

%prep

%build
# intentionally left blank

%install
# selinux policies
mkdir -p $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux
install -m 644 %{_topdir}/../%{SOURCE1} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{_topdir}/../%{SOURCE2} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{_topdir}/../%{SOURCE3} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/

# misp-workers.service
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
install -m 644 %{_topdir}/../%{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system

mkdir -p $RPM_BUILD_ROOT/usr/share/httpd/.cache

mkdir -p $RPM_BUILD_ROOT/var/www

# pecl - redis
echo '' | sudo /opt/rh/rh-%{phprpm}/root/usr/bin/pecl install -f redis
mkdir -p $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules
cp {,$RPM_BUILD_ROOT}/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules/redis.so

# pecl - ssdeep
# ssdeep hard codes /usr/lib for libfuzzy.so
sudo ln -sf /usr/lib64/libfuzzy.so /usr/lib/libfuzzy.so
echo '' | sudo /opt/rh/rh-%{phprpm}/root/usr/bin/pecl install -f ssdeep
mkdir -p $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules
cp {,$RPM_BUILD_ROOT}/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules/ssdeep.so

# pear - Crypt_GPG
echo '' | sudo /opt/rh/rh-%{phprpm}/root/usr/bin/pear install -f Crypt_GPG
mkdir -p $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/share/pear-data
mkdir -p $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/share/pear
cp -r /opt/rh/rh-%{phprpm}/root/usr/share/pear-data/Crypt_GPG $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/share/pear-data/
cp -r /opt/rh/rh-%{phprpm}/root/usr/share/pear/Crypt $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/share/pear/

# upstream brotli
git clone -b %{phpbrotliver} --depth 1 https://github.com/kjdev/php-ext-brotli $RPM_BUILD_ROOT/var/tmp/php-ext-brotli
pushd $RPM_BUILD_ROOT/var/tmp/php-ext-brotli
git submodule sync
git submodule update --init --recursive
/opt/rh/rh-%{phprpm}/root/usr/bin/phpize
./configure --with-php-config=/opt/rh/rh-%{phprpm}/root/usr/bin/php-config
make
mkdir -p $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules
# remove path from symbols so that check-buildroot doesn't complain
strip --strip-debug modules/brotli.so
cp modules/brotli.so $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules/brotli.so
popd
# and cleanup any trace to make check-buildroot happy (again) ...
rm -rf $RPM_BUILD_ROOT/var/tmp/php-ext-brotli

# pecl - rdkafka
echo '' | sudo /opt/rh/rh-%{phprpm}/root/usr/bin/pecl install -f rdkafka
mkdir -p $RPM_BUILD_ROOT/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules
cp {,$RPM_BUILD_ROOT}/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules/rdkafka.so

git clone -b v%{mispver} --depth 1 https://github.com/MISP/MISP.git $RPM_BUILD_ROOT/var/www/MISP

pushd $RPM_BUILD_ROOT/var/www/MISP
	git submodule sync
	git submodule update --init --recursive
	git submodule foreach --recursive git config core.filemode false
	git config core.filemode false
popd

# create python3 virtualenv
/opt/rh/rh-%{pyrpm}/root/usr/bin/python3 -m venv --copies $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv

$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U pip setuptools wheel

for pymod in python-cybox python-stix mixbox cti-python-stix2 python-maec; do
	$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install $RPM_BUILD_ROOT/var/www/MISP/app/files/scripts/$pymod
done

for pymod in zmq redis python-magic plyara pydeep lief; do
	$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U $pymod
done

$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U $RPM_BUILD_ROOT/var/www/MISP/PyMISP

# virtualenv PATH mess fixup
rm -rf $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/__pycache__
find $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv -name 'direct_url.json' -type f -delete

sed -i -r -e 's@#!/.*python3@/var/www/cgi-bin/misp-virtualenv/bin/python3@' $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -i -r -e 's@(VIRTUAL_ENV[= ])"(.*/var/www/cgi-bin/misp-virtualenv)"@\1"/var/www/cgi-bin/misp-virtualenv"@' $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/activate*
# EO python setup

# CakePHP
pushd $RPM_BUILD_ROOT/var/www/MISP/app
	/opt/rh/rh-%{phprpm}/root/usr/bin/php composer.phar install
popd

# cleanup
find $RPM_BUILD_ROOT/var/www/ \
	   -name '.git' \
	-o -name '.github' \
	-o -name '.gitignore' \
	-o -name '.gitmodules' \
	-o -name '.travis.yml' \
	-print0 | xargs -0 rm -rf

chmod g+w $RPM_BUILD_ROOT/var/www/MISP/app/Config

%files python-virtualenv
%defattr(-,apache,apache,-)
/var/www/cgi-bin/misp-virtualenv

# TODO "extension=redis.so" to php.ini
%files pecl-redis
/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules/redis.so

# TODO "extension=ssdeep.so" to php.ini
%files pecl-ssdeep
/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules/ssdeep.so

%files pear-crypt-gpg
/opt/rh/rh-php73/root/usr/share/pear/Crypt
/opt/rh/rh-php73/root/usr/share/pear-data/Crypt_GPG

# TODO "extension=brotli.so" to php.ini
%files php-brotli
/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules/brotli.so

# TODO "extension=rdkafka.so" to php.ini
%files pecl-rdkafka
/opt/rh/rh-%{phprpm}/root/usr/lib64/php/modules/rdkafka.so

%files
%defattr(-,apache,apache,-)
%config(noreplace) /var/www/MISP/app/Plugin/CakeResque/Config/config.php
/var/www/MISP
%defattr(-,root,root,-)
/usr/share/MISP/policy/selinux/misp-*.pp
%{_sysconfdir}/systemd/system/misp-workers.service
# exclude test files whicht get detected by AV solutions
%exclude /var/www/MISP/PyMISP/tests

%post
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

%changelog
* Thu May 12 2022 Rémi Laurent <remi.laurent@securitymadein.lu> - 2.4.155
- update to 2.4.155 and RHEL 7.9 packaging without external repos

* Thu Oct 14 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.150
- update to 2.4.150

* Mon Sep 13 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.148-2
- update to include some important patches

* Wed Aug 11 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.148
- update to 2.4.148

* Tue Jul 28 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.147
- update to 2.4.147

* Tue Jul 6 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.146
- update to 2.4.146

* Wed Jun 30 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.145
- update to 2.4.145

* Tue Jun 8 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.144
- update to 2.4.144

* Fri May 21 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.143
- update to 2.4.143

* Sat Apr 24 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.141
- new build process to put all python modules into a virtual environment
