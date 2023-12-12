# spec file for ssdeep
#
# Copyright (c) 2014-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#

Name:      ssdeep
Version:   2.14.1
Release:   2%{?dist}
Summary:   Compute context triggered piecewise hashes
Group:     Development/Tools

License:   GPLv2+
URL:       https://ssdeep-project.github.io/ssdeep/
Source0:   https://github.com/ssdeep-project/ssdeep/releases/download/release-%{version}/ssdeep-%{version}.tar.gz

Requires:  %{name}-libs%{?_isa} = %{version}-%{release}


%description
ssdeep is a program for computing context triggered piecewise hashes (CTPH).
Also called fuzzy hashes, CTPH can match inputs that have homologies.
Such inputs have sequences of identical bytes in the same order, although bytes
in between these sequences may be different in both content and length.


%package devel
Summary: Development files for libfuzzy
Group:   Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains library and header files for
developing applications that use libfuzzy.


%package libs
Summary: Runtime libfuzzy library
Group:   System Environment/Libraries

%description libs
The %{name}-libs package contains libraries needed by applications
that use libfuzzy.


%prep
%setup -q

# avoid autotools being re-run
touch -r aclocal.m4 configure configure.ac


%build
%configure \
   --disable-auto-search \
   --disable-static

# rpath removal
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# "hack" to be able to build rh-php73-pecl-ssdeep
mkdir -p %{buildroot}/usr/lib
cd %{buildroot}/usr/lib
ln -s ../lib64/libfuzzy.so.2.1.0 ./libfuzzy.so
ln -s ../include/fuzzy.h ./fuzzy.h
ln -s ../include/fuzzy.h ../lib64/fuzzy.h


rm %{buildroot}%{_libdir}/libfuzzy.la


%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%doc AUTHORS
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.*

%files devel
%doc FILEFORMAT NEWS README TODO
%{_includedir}/fuzzy.h
%{_includedir}/edit_dist.h
%{_libdir}/libfuzzy.so
/usr/lib/libfuzzy.so
/usr/lib/fuzzy.h
/usr/lib64/fuzzy.h

%files libs
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/libfuzzy.so.2*
/usr/lib/libfuzzy.so


%changelog
* Thu Nov 23 2023 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 2.14.1-2
- added link from lib64 to lib, for building rh-php73 pecl extension

* Tue Nov  7 2017 Remi Collet <remi@fedoraproject.org> - 2.14.1-1
- update to 2.14.1

* Fri Sep 15 2017 Remi Collet <remi@fedoraproject.org> - 2.14-1
- update to 2.14
- sources from github
- fix project URL

* Tue May  5 2015 Remi Collet <remi@fedoraproject.org> - 2.13-1
- update to 2.13

* Sun Oct 26 2014 Remi Collet <remi@fedoraproject.org> - 2.12-1
- update to 2.12
- fix license handling

* Fri Sep 12 2014 Remi Collet <remi@fedoraproject.org> - 2.11-1
- update to 2.11

* Wed Jan 22 2014 Remi Collet <remi@fedoraproject.org> - 2.10-2
- cleanup build path (comment from review #1056460)

* Wed Jan 22 2014 Remi Collet <remi@fedoraproject.org> - 2.10-1
- initial package
