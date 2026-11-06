# get number from dist variable
%global dist_num %(echo "%{?dist}" | grep -o -E '[0-9]+')

Name:       misp-release	
Version:	2.0
Release:	1%{?dist}
Summary:	configuration for MISP repositories for EL%{dist}

Group:		System Environment/Base
License:	GPLv2
URL:		https://repo.misp-project.ch/yum/misp%{dist_num}/
Source0:	misp%{dist_num}.repo
Source1:	RPM-GPG-KEY-KOJI-MISPPROJECT-EL%{dist_num}

BuildArch:  	noarch

%description
Configuration for MISP repositories (Mariadb and MISP) for EL%{dist_num}

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
%config /etc/yum.repos.d/*
/etc/pki/rpm-gpg/RPM-GPG-KEY-KOJI-MISPPROJECT-EL%{dist_num}

%changelog
* Tue Nov 3 2026 Andreas Muehlemann <amuehlem@gmail.com> - 2.0
- adapting to new MISP-RPM setup

* Mon Aug 18 2025 Andreas Muehlemann <amuehlem@gmail.com> - 1.0
- first version for EL10
