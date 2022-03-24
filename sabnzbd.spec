%global user %{name}
%global group %{name}
%global __python %{__python3}

Name:           sabnzbd
Version:        3.5.3
Release:        1%{?dist}
Summary:        The automated Usenet download tool
License:        GPLv2+
URL:            https://sabnzbd.org/
BuildArch:      noarch

Source0:        https://github.com/%{name}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        config.ini
Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  firewalld-filesystem
BuildRequires:  python3
BuildRequires:  systemd
BuildRequires:  tar

Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       par2cmdline
Requires:       python3
Requires:       python3-chardet
Requires:       python3-cheetah
Requires:       python3-cheroot
Requires:       python3-cherrypy
Requires:       python3-configobj
Requires:       python3-cryptography
Requires:       python3-feedparser
Requires:       python3-guessit
Requires:       python3-notify2
Requires:       python3-portend
Requires:       python3-puremagic
Requires:       python3-sabyenc
Requires:       rar
Requires(pre):  shadow-utils

%description
It's totally free, easy to use, and works practically everywhere. SABnzbd makes
Usenet as simple and streamlined as possible by automating everything we can.
All you have to do is add an .nzb. SABnzbd takes over from there, where it will
be automatically downloaded, verified, repaired, extracted and filed away with
zero human interaction. SABnzbd offers an easy setup wizard and has
self-analysis tools to verify your setup.

%prep
%autosetup -n %{name}-%{version}

%build
tools/make_mo.py

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

cp -fr SABnzbd.py sabnzbd po interfaces icons email locale %{buildroot}%{_datadir}/%{name}

install -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/config.ini
install -m 0644 -p %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 -p %{SOURCE11} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml

# Always invoke Python 3
find %{buildroot} -name "*.py" -exec sed -i \
    -e 's|/usr/bin/env python$|/usr/bin/env python3|g' {} \;

# rpmlint fixes
find %{buildroot} \( -name "*.js" -o -name "*.css" -o -name "*.txt  " \) -exec chmod 644 {} \;
chmod 755 $(grep -RH '/usr/bin/' %{buildroot}%{_datadir}/%{name} | cut -d: -f1)

%find_lang SABnzbd

%pre
getent group %{group} >/dev/null || groupadd -r %{group}
getent passwd %{user} >/dev/null || \
    useradd -r -g %{group} -d %{_sharedstatedir}/%{name} -s /sbin/nologin \
    -c "%{name}" %{user}
exit 0

%post
%systemd_post %{name}.service
%firewalld_reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files -f SABnzbd.lang
%license LICENSE.txt
%doc README.md README.mkd ISSUES.txt
%attr(750,%{user},%{group}) %{_sharedstatedir}/%{name}
%dir %attr(750,%{user},%{group}) %{_sysconfdir}/%{name}
%config(noreplace) %attr(644,%{user},%{group}) %{_sysconfdir}/%{name}/config.ini
%{_datadir}/%{name}
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_unitdir}/%{name}.service
%attr(750,%{user},%{group}) %{_localstatedir}/log/%{name}

%changelog
* Thu Mar 24 2022 Simone Caronni <negativo17@gmail.com> - 3.5.3-1
- Update to 3.5.3.

* Thu Mar 10 2022 Simone Caronni <negativo17@gmail.com> - 3.5.2-1
- Update to 3.5.2.

* Fri Feb 25 2022 Simone Caronni <negativo17@gmail.com> - 3.5.1-1
- Update to 3.5.1.

* Fri Feb 04 2022 Simone Caronni <negativo17@gmail.com> - 3.5.0-1
- Update to 3.5.0.

* Thu Dec 16 2021 Simone Caronni <negativo17@gmail.com> - 3.4.2-2
- Fix runtime requirements.

* Fri Oct 15 2021 Simone Caronni <negativo17@gmail.com> - 3.4.2-1
- Update to 3.4.2.

* Fri Sep 24 2021 Simone Caronni <negativo17@gmail.com> - 3.4.1-1
- Update to 3.4.1.

* Mon Sep 20 2021 Simone Caronni <negativo17@gmail.com> - 3.4.0-1
- Update to 3.4.0.

* Sun Jun 20 2021 Simone Caronni <negativo17@gmail.com> - 3.3.1-1
- Update to 3.3.1.

* Mon Jun 07 2021 Simone Caronni <negativo17@gmail.com> - 3.3.0-1
- Update to 3.3.0.

* Wed May 05 2021 Simone Caronni <negativo17@gmail.com> - 3.2.1-1
- Update to 3.2.1.

* Sun Mar 07 2021 Simone Caronni <negativo17@gmail.com> - 3.2.0-1
- Update to 3.2.0.

* Tue Nov 17 2020 Simone Caronni <negativo17@gmail.com> - 3.1.1-1
- Update to 3.1.1.

* Thu Nov 05 2020 Simone Caronni <negativo17@gmail.com> - 3.1.0-1
- Update to 3.1.0.

* Tue Oct 06 2020 Simone Caronni <negativo17@gmail.com> - 3.0.2-1
- Update to 3.0.2.

* Tue Aug 25 2020 Simone Caronni <negativo17@gmail.com> - 3.0.1-1
- Update to 3.0.1.

* Sun Aug 16 2020 Simone Caronni <negativo17@gmail.com> - 3.0.0-4
- Update to final 3.0.0.

* Sun Jun 28 2020 Simone Caronni <negativo17@gmail.com> - 3.0.0-3
- Update to 3.0.0RC1.
- Fix typo in requirements.

* Mon Jun 22 2020 Simone Caronni <negativo17@gmail.com> - 3.0.0-2
- Update to 3.0.0 Beta 4.
- Fix requirements.

* Tue May 26 2020 Simone Caronni <negativo17@gmail.com> - 3.0.0-1
- Update to 3.0.0 Alpha 2.
- Fix description and summary.
- Rpmling fixes.

* Sun Dec 01 2019 Simone Caronni <negativo17@gmail.com> - 2.3.9-2
- Add default configuration file.

* Sun Nov 17 2019 Simone Caronni <negativo17@gmail.com> - 2.3.9-1
- First build.
