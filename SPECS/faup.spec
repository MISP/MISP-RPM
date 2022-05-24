%define cmake cmake3 -DCMAKE_INSTALL_PREFIX:PATH=/usr
# no upstream tags/releases for a while - let's use git commitid
%define version 1.6.0
%define cid 8e81b17

Name:		faup
Version:	%{version}+%{cid}
Release:	1%{?dist}
Summary:    	Fast URL decoder library
License:    	Public

Group:		Development/Languages
URL:		https://github.com/stricaud/faup/
Source0:	fake-tgz.tgz

BuildRequires: cmake3, gtcaca-devel, git
Requires: gtcaca

%description
Fast URL decoder library https://github.com/stricaud/faup/

%package devel
Summary: Files needed to build faup

%description devel
This package contains the files needed for building faup extensions. 

%build
rm -rf faup
git clone https://github.com/stricaud/faup.git faup
cd faup
git reset --hard %{cid}
mkdir -p build
cd build
%cmake ..
make %{?_smp_mflags}

%install
cd faup/build/
%make_install

%files
/usr/bin/faup
%{_libdir}/pkgconfig/faup.pc
%{_libdir}/libfaupl.so
%{_libdir}/libfaupl.so.1
%dir /usr/share/faup
/usr/share/faup/README.txt
/usr/share/faup/modules_available/emulation_ie.lua
/usr/share/faup/modules_available/ipv4toint.lua
/usr/share/faup/modules_available/printcsv.lua
/usr/share/faup/modules_available/redis-url-threatintel.lua
/usr/share/faup/modules_available/uppercase.lua
/usr/share/faup/modules_available/writeall.lua
/usr/share/faup/modules_available/writeinput.lua
/usr/share/faup/mozilla.tlds
/usr/share/man/man1/faup.1.gz

%files devel
%dir /usr/include/faup
/usr/include/faup/*.h

%changelog
* Tue May 24 2022 Rémi Laurent <remi.laurent@securitymadein.lu>
- bound version and git commit id

* Wed Jun 30 2021 Andreas Muehlemann <andreas.muehlemann@swithc.ch>
- version 1.6
- clone from git

* Mon May 25 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch>
- added cmake macro, changed source0 to not interfere with other master.tar.gz

* Sun May 24 2020 Todd E Johnson <todd@toddejohnson.net>
- first version
