%global php_inidir  %{_sysconfdir}/php.d
%global pecl_name   ssdeep
%global pecl_xmldir /var/lib/pear/pkgxml
%global php_extdir /usr/lib64/php/modules/
%global __brp_check_rpaths %{nil}

Name:       misp-php-pecl-ssdeep
Version:    1.1.0
Release:    2%{?dist}
Summary:    PHP extension for interfacing ssdeep

Obsoletes:	misp-php82-pecl-ssdeep = 1.1.0

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phpssdeep/phpssdeep/
Source0:    https://pecl.php.net/get/ssdeep-%{version}.tgz
Source1:    ssdeep-2.14.1.tar.gz

Patch0:	    https://patch-diff.githubusercontent.com/raw/php/pecl-text-ssdeep/pull/2.patch

BuildRequires:  php, php-devel
BuildRequires: 	php-cli, php-pear
BuildRequires:	ssdeep, ssdeep-devel, patch
Requires:       php

%description
PHP extension for interfacing ssdeep

%prep
%setup -q -n ssdeep-%{version}

cd ..
tar xzf %{SOURCE1}
cd ssdeep-2.14.1
touch -r aclocal.m4 configure configure.ac
%configure \
   --disable-auto-search \
   --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

cd ../ssdeep-%{version}

# create the ini file
cat > %{pecl_name}.ini << EOF
extension=%{pecl_name}.so
EOF

%build
# patch for php8
patch -p1 < %{PATCH0}

# ssdeep hard codes /usr/lib for libfuzzy.so
phpize
./configure \
    --with-ssdeep=../ssdeep-2.14.1 \
    --with-php-config=/usr/bin/php-config
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pecl_name}.ini %{buildroot}/etc/php.d/%{pecl_name}.ini

%files
%{php_extdir}/%{pecl_name}.so
%config(noreplace) /etc/php.d/%{pecl_name}.ini
%exclude /usr/lib/.build-id*

%changelog
* Sat Aug 30 2025 Andreas Muehlemann <amuehlem@gmail.com> - 1.2.2
- renaming the package

* Tue Feb 4 2025 Andreas Muehlemann <amuehlem@gmail.com> - 5.3.7
- first version for php82
