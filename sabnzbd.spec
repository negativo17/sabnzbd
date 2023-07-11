%global user %{name}
%global group %{name}

%global desktop_id org.sabnzbd.sabnzbd

Name:           sabnzbd
Version:        4.0.3
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
BuildRequires:  libappstream-glib
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
Requires:       python3-sabctools
Requires:       python3-sabyenc >= 5.4.4
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
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

cp -fr SABnzbd.py sabnzbd po interfaces icons email locale %{buildroot}%{_datadir}/%{name}

install -m 0644 -p -D %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/config.ini
install -m 0644 -p -D %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 -p -D %{SOURCE11} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml
install -m 0644 -p -D linux/sabnzbd.bash-completion %{buildroot}%{_sysconfdir}/bash_completion.d/sabnzbd
install -m 0644 -p -D linux/%{desktop_id}.appdata.xml %{buildroot}%{_metainfodir}/%{desktop_id}.appdata.xml

# Always invoke Python 3
find %{buildroot} -name "*.py" -exec sed -i \
    -e 's|/usr/bin/env python.*|/usr/bin/python3|g' {} \;

# rpmlint fixes
find %{buildroot} \( -name "*.js" -o -name "*.css" -o -name "*.txt  " \) -exec chmod 644 {} \;
chmod 755 $(grep -RH '/usr/bin/' %{buildroot}%{_datadir}/%{name} | cut -d: -f1)


%check
%if 0%{?fedora}
# Url validator broken on el7, 8 and 9: https://bugzilla.redhat.com/show_bug.cgi?id=2119708
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{desktop_id}.appdata.xml
%endif

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
%{_metainfodir}/%{desktop_id}.appdata.xml
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_sysconfdir}/bash_completion.d/sabnzbd
%{_unitdir}/%{name}.service
%attr(750,%{user},%{group}) %{_localstatedir}/log/%{name}

%changelog
* Tue Jul 11 2023 Simone Caronni <negativo17@gmail.com> - 4.0.3-1
- Update to 4.0.3.

* Mon Jun 12 2023 Simone Caronni <negativo17@gmail.com> - 4.0.2-1
- Update to 4.0.2.

* Sat May 27 2023 Simone Caronni <negativo17@gmail.com> - 4.0.1-1
- Update to 4.0.1.
- Trim changelog.

* Mon Feb 06 2023 Simone Caronni <negativo17@gmail.com> - 3.7.2-1
- Update to 3.7.2.
- Add AppData information.
- Add bash completion.
- Expand systemd unit.

* Sun Nov 06 2022 Simone Caronni <negativo17@gmail.com> - 3.7.0-1
- Update to 3.7.0.

* Sun Sep 25 2022 Simone Caronni <negativo17@gmail.com> - 3.6.1-1
- Update to 3.6.1.

* Thu Jun 16 2022 Simone Caronni <negativo17@gmail.com> - 3.6.0-1
- Update to 3.6.0.

* Thu Mar 24 2022 Simone Caronni <negativo17@gmail.com> - 3.5.3-1
- Update to 3.5.3.

* Thu Mar 10 2022 Simone Caronni <negativo17@gmail.com> - 3.5.2-1
- Update to 3.5.2.

* Fri Feb 25 2022 Simone Caronni <negativo17@gmail.com> - 3.5.1-1
- Update to 3.5.1.

* Fri Feb 04 2022 Simone Caronni <negativo17@gmail.com> - 3.5.0-1
- Update to 3.5.0.
