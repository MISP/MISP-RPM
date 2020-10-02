Name:       	misp-release	
Version:	1.0
Release:	1%{?dist}
Summary:	configuration for MISP repositories for EL8

Group:		System Environment/Base
License:	GPLv2
URL:		https://cruncher.switch.ch/repos/
Source0:	misp8.repo
Source1:    	RPM-GPG-KEY-KOJI-SWITCH

BuildArch:  	noarch

%description
Configuration for MISP repositories (Mariadb and MISP) for EL8

%prep
%setup -q -c -T

%build

%install
rm -rf $RPM_BUILD_ROOT

install -dm 755 $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/yum.repos.d/misp.repo
install -dm 744 $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg
install -pm 644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/pki/rpm-gpg

%files
%defattr(-,root,root,-)
%config(noreplace) /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-KOJI-SWITCH

%changelog
* Wed Sep 30 2020 Andreas Muehlemann <andreas.muehlemann@switch.ch> - 1.0
- first version for EL8
