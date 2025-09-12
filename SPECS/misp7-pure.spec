%global __python %{__python3}
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global _python_bytecompile_extra 0
%define _binaries_in_noarch_packages_terminate_build 0
# disable mangling of shebangs #!
%define __brp_mangle_shebangs /usr/bin/true
# exclude for requirements
%global __requires_exclude ^/opt/python/cp3.*

# upstream MISP main version
%define mispver 2.4.204
%define pymispver 2.4.198
# you can ship package level releases with the Release version value
# defaults to -1.el7 for RHEL7
%define rpmver 1
%define phprpm php73
%define pyrpm python38

%define _scl_php_loader /usr/bin/scl enable rh-%{phprpm}

Name:		misp
Version:	%{mispver}
Release:	%{rpmver}%{?dist}
Summary:	MISP - malware information sharing platform

Group:		Internet Applications
License:	GPLv3
URL:		http://www.misp-project.org/
Source1:	misp-httpd.pp
Source2:	misp-bash.pp
Source3:	misp-ps.pp
Source4:	misp-workers.service
Patch0:         MISP-AppModel.php.patch

#BuildRequires:	/usr/bin/pathfix.py
BuildRequires:	git, rh-%{pyrpm}-python-devel, rh-%{pyrpm}-python-pip, libxslt-devel, zlib-devel
BuildRequires:	rh-%{phprpm}-php, rh-%{phprpm}-php-cli, rh-%{phprpm}-php-xml, rh-%{phprpm}-php-mbstring
BuildRequires:  rh-%{phprpm}-php-pear, rh-%{phprpm}-php-devel
BuildRequires:  ssdeep-libs, ssdeep-devel
BuildRequires:  librdkafka librdkafka-devel
BuildRequires:	cmake3, bash-completion
Source0:	fake-tgz.tgz
Source1:        misp.conf
Source2:        misp-httpd.pp
Source3:        misp-bash.pp
Source4:        misp-ps.pp
Source5:        misp-workers.service
Source6:        start-misp-workers.sh
Source7:	misp-workers.ini
Patch0:         MISP-AppModel.php.patch

BuildRequires:	/usr/bin/pathfix.py
BuildRequires:	git, misp-python, libxslt-devel, zlib-devel
BuildRequires:	php74-php, php74-php-cli, php74-php-xml, php74-php-mbstring
BuildRequires:	ssdeep-devel, cmake3, bash-completion
BuildRequires:	libcaca-devel
BuildRequires:	wget

Requires:	httpd24, httpd24-mod_ssl, rh-redis6-redis, libxslt, zlib
Requires:	rh-mariadb105-mariadb, rh-mariadb105-mariadb-server
Requires:	rh-%{pyrpm}-python, misp-python-virtualenv
Requires:	rh-%{phprpm}-php, rh-%{phprpm}-php-cli, rh-%{phprpm}-php-gd, rh-%{phprpm}-php-pdo
Requires:	rh-%{phprpm}-php-mysqlnd, rh-%{phprpm}-php-mbstring, rh-%{phprpm}-php-xml
Requires:       rh-%{phprpm}-php-bcmath, rh-%{phprpm}-php-opcache, rh-%{phprpm}-php-json
Requires:       rh-%{phprpm}-php-zip, misp-%{phprpm}-pecl-redis, rh-%{phprpm}-php-intl
Requires:       misp-%{phprpm}-pear-crypt-gpg, misp-%{phprpm}-pecl-ssdeep, ssdeep-libs
Requires:	misp-%{phprpm}-pecl-brotli, misp-%{phprpm}-pecl-rdkafka
Requires:	gtcaca faup

%package python-virtualenv
Summary:        the python virtual environment for MISP
Group:          Internet Applications
License:        GPLv3

%description python-virtualenv
The python vitualenvironment for MISP

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
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT/usr/share/MISP/policy/selinux/

# misp-workers.service
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/systemd/system

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/default
echo "SCL_PHP_WRAPPER=/usr/bin/scl enable rh-%{phprpm}" > $RPM_BUILD_ROOT%{_sysconfdir}/default/misp-workers
# patch app/Model/Server.php to show commit ID
patch --ignore-whitespace -p0 < %{PATCH0}

# create python3 virtualenv
/var/www/cgi-bin/misp-python/bin/python3 -m venv --copies $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv

mkdir -p $RPM_BUILD_ROOT/usr/share/httpd/.cache

mkdir -p $RPM_BUILD_ROOT/var/www

git clone -b v%{mispver} --depth 1 https://github.com/MISP/MISP.git $RPM_BUILD_ROOT/var/www/MISP

pushd $RPM_BUILD_ROOT/var/www/MISP
	git submodule sync
	git submodule update --init --recursive
	git submodule foreach --recursive git config core.filemode false
	git config core.filemode false


	# patch app/Model/Server.php to show commit ID
	patch --ignore-whitespace -p0 < %{PATCH0}

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

$RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/pip install -U pymisp==%{pymispver}

# virtualenv PATH mess fixup
rm -rf $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/__pycache__
find $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv -name 'direct_url.json' -type f -delete

sed -i -r -e 's@#!/.*python3@/var/www/cgi-bin/misp-virtualenv/bin/python3@' $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -i -r -e 's@(VIRTUAL_ENV[= ])"(.*/var/www/cgi-bin/misp-virtualenv)"@\1"/var/www/cgi-bin/misp-virtualenv"@' $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/activate*
# EO python setup

# CakePHP
pushd $RPM_BUILD_ROOT/var/www/MISP/app
	sed -i composer.json -e 's/"php": ">=7.4.0,<8.0.0",/"php": ">=7.3.0,<8.0.0",/g'
	/opt/rh/rh-%{phprpm}/root/usr/bin/php composer.phar install
popd
cd $RPM_BUILD_ROOT/var/www/MISP/app
/opt/remi/php74/root/usr/bin/php composer.phar install
/opt/remi/php74/root/usr/bin/php composer.phar require supervisorphp/supervisor:^4.0 guzzlehttp/guzzle php-http/message lstrojny/fxmlrpc

cd $RPM_BUILD_ROOT/var/www/MISP
# save commit ID of this installation
git rev-parse HEAD > .git_commit_version

# clean up before PATH rewriting
rm -rf $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/__pycache__

# rewrite PATH in virtualenv
sed -e "s/\/usr\/local\/bin\/python3.9/\/var\/www\/cgi-bin\/misp-virtualenv\/bin\/python3/g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/bin/*
sed -e "s/\/builddir\/build\/BUILDROOT\/%{name}-%{version}-%{release}.%{_arch}//g" -i $RPM_BUILD_ROOT/var/www/cgi-bin/misp-virtualenv/lib/python3.9/site-packages/pymisp-%{pymispver}.dist-info/direct_url.json

# path fix for python3
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" . $RPM_BUILD_ROOT/var/www/MISP/*

# cleanup
find $RPM_BUILD_ROOT/var/www/ \
	   -name '.git' \
	-o -name '.github' \
	-o -name '.gitignore' \
	-o -name '.gitmodules' \
	-o -name '.travis.yml' \
	-print0 | xargs -0 rm -rf

chmod g+w $RPM_BUILD_ROOT/var/www/MISP/app/Config
mkdir -p $RPM_BUILD_ROOT/etc/supervisord.d
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT/etc/supervisord.d
%files python-virtualenv
%defattr(-,apache,apache,-)
/var/www/cgi-bin/misp-virtualenv

%files
%defattr(-,apache,apache,-)
%config(noreplace) /var/www/MISP/app/Plugin/CakeResque/Config/config.php
/var/www/MISP
%config(noreplace) /etc/httpd/conf.d/misp.conf
%config(noreplace) /etc/supervisord.d/misp-workers.ini
/usr/share/MISP/policy/selinux/misp-*.pp
%{_sysconfdir}/systemd/system/misp-workers.service
%defattr(-,root,root,-)
/usr/share/MISP/policy/selinux/misp-*.pp
%{_sysconfdir}/default/misp-workers
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
systemctl restart supervisor

%changelog
* Thu Feb 6 2025 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.204
- update to 2.4.204

* Fri Sep 20 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.198
- update to 2.4.198

* Thu Jul 11 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.194
- update to 2.4.194

* Mon Apr 22 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.191
- update to 2.4.191

* Tue Apr 02 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.188
- update to 2.4.188

* Tue Mar 12 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.187
- update to 2.4.187

* Fri Feb 23 2024 Andreas Muehlemann <amuehlem@gmail.com> - 2.4.185
- update to 2.4.185

* Fri Feb 9 2024 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.184
- update to 2.4.184

* Thu Jan 18 2024 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.183
- update to 2.4.183

* Tue Dec 19 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.182
- update to 2.4.182

* Mon Dec 4 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.181
- update to 2.4.181, fix for php 7.3

* Mon Nov 27 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.179
- update to 2.4.179

* Fri Nov 24 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.177
- update to 2.4.177, adaption to koji build environment

* Wed Jul 6 2022 Rémi Laurent <remi.laurent@securitymadein.lu> - 2.4.159
- update to 2.4.159 and shipping extra required EPEL packages

* Tue May 24 2022 Rémi Laurent <remi.laurent@securitymadein.lu> - 2.4.158
- update to 2.4.158

* Thu May 12 2022 Rémi Laurent <remi.laurent@securitymadein.lu> - 2.4.155
- update to 2.4.155 and RHEL 7.9 packaging without external repos
* Tue Apr 26 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.158
- update to 2.4.158

* Fri Mar 25 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.157
- udpate to 2.4.157

* Sun Mar 20 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.156
- update to 2.4.156

* Fri Mar 4 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.155
- update to 2.4.155
- added requirement for misp-python, because of pymisp needing python >= 3.7

* Mon Feb 7 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.153
- update to 2.4.153
- added supervisor for background tasks
- added php-apcu and php-process as requirements
 
* Mon Jan 10 2022 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.152
- new build to solve MISP issues #8057

* Mon Dec 27 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.152
- update to 2.4.152

* Thu Dec 02 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.151
- update to 2.4.151

* Thu Oct 14 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.150
- update to 2.4.150

* Mon Sep 13 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.148-2
- update to include some important patches

* Wed Aug 11 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.148
- update to 2.4.148

* Wed Jul 28 2021 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.4.147
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

