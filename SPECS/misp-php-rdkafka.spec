%global php_inidir  %{_sysconfdir}/php.d
%global pie_proj   rdkafka
%global pecl_xmldir /var/lib/pear/pkgxml
%global php_extdir /usr/lib64/php/modules/

Name:       misp-php-rdkafka
Version:    6.0.4
Release:    1%{?dist}
Summary:    PHP extension for interfacing rdkafka

Obsoletes:	misp-php82-pecl-rdkafka < 6.0.0
Conflicts:	misp-php82-pecl-rdkafka < 6.0.0

Group:      Development/Languages
License:    PHP
URL:        https://github.com/phprdkafka/phprdkafka/

BuildRequires:  git
BuildRequires:  php, php-devel
BuildRequires: 	php-cli, php-pear
BuildRequires:	librdkafka librdkafka-devel
Requires:       php

%description
PHP extension for interfacing rdkafka

%prep
%setup -qTc

# install from git
git clone https://github.com/arnaud-lb/php-rdkafka.git
cd php-rdkafka

%build
cd php-rdkafka
phpize
%configure \
    --enable-rdkafka \
    --with-php-config=/usr/bin/php-config \
    --with-libdir=%{_lib}

make %{?_smp_mflags}

# create the ini file
cat > %{pie_proj}.ini << EOF
extension=%{pie_proj}.so
EOF

%install
cd php-rdkafka
make install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{pie_proj}.ini %{buildroot}/etc/php.d/%{pie_proj}.ini

%files
%{php_extdir}/%{pie_proj}.so
%config(noreplace) /etc/php.d/%{pie_proj}.ini

%changelog
* Wed Oct 28 2026 Andreas Muehlemann <amuehlem@gmail.com> - 6.0.4
- renaming the package
- update to 6.0.4
