%global php_inidir  %{_sysconfdir}/php.d
%global pie_vend    kjdev
%global pie_proj    brotli
%global pecl_xmldir /var/lib/pear/pkgxml
%global php_extdir /usr/lib64/php/modules/

Name:       misp-php-brotli
Version:    0.21.1
Release:    1%{?dist}
Summary:    PHP extension for interfacing brotli

Obsoletes:	misp-php82-pecl-brotli < 0.15
Conflicts:	misp-php82-pecl-brotli < 0.15

Group:      Development/Languages
License:    MIT 
URL:        https://github.com/kjdev/php-ext-brotli

BuildRequires:  git
BuildRequires:  php, php-devel
BuildRequires: 	php-cli, php-pear
BuildRequires:	brotli, brotli-devel
Requires:       php

%description
PHP extension for interfacing brotli

%prep
%setup -qTc

# install from git
git clone --recursive --depth=1 https://github.com/kjdev/php-ext-brotli.git

%build
# brotli hard codes /usr/lib for libfuzzy.so
cd php-ext-brotli
rm -rf brotli
phpize
./configure \
    --with-php-config=/usr/bin/php-config \
    --with-libbrotli \
    --with-libdir=%{_lib} \
    --enable-brotli

make %{?_smp_mflags}

# create the ini file
cat > %{pie_proj}.ini << EOF
extension=%{pie_proj}.so
EOF

%install
cd php-ext-brotli
make install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pie_proj}.ini %{buildroot}/etc/php.d/%{pie_proj}.ini

%files
%{php_extdir}/%{pie_proj}.so
%config(noreplace) /etc/php.d/%{pie_proj}.ini

%changelog
* Wed Oct 28 2026 Andreas Muehlemann <amuehlem@gmail.com> - 0.21.1
- renaming the package
- update to 0.21.1
