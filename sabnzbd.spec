%global user %{name}
%global group %{name}

Name:           sabnzbd
Version:        5.0.4
Release:        1%{?dist}
Summary:        The automated Usenet download tool
License:        GPLv2+
URL:            https://sabnzbd.org/
BuildArch:      noarch

Source0:        https://github.com/%{name}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        config.ini
# Adjusted requirements. Simpler than making a patch:
Source2:        %{name}-requirements.txt
Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  firewalld-filesystem
BuildRequires:  python3-devel
BuildRequires:  systemd
BuildRequires:  tar

Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       par2cmdline
Requires:       python3-rarfile
Requires:       rar

%description
It's totally free, easy to use, and works practically everywhere. SABnzbd makes
Usenet as simple and streamlined as possible by automating everything we can.
All you have to do is add an .nzb. SABnzbd takes over from there, where it will
be automatically downloaded, verified, repaired, extracted and filed away with
zero human interaction. SABnzbd offers an easy setup wizard and has
self-analysis tools to verify your setup.

%prep
%autosetup -n %{name}-%{version}
cp -f %{SOURCE2} requirements.txt
%generate_buildrequires
%pyproject_buildrequires -N requirements.txt

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

# Always invoke Python 3
find %{buildroot} -name "*.py" -exec sed -i \
    -e 's|/usr/bin/env python.*|/usr/bin/python3|g' {} \;

# rpmlint fixes
find %{buildroot} \( -name "*.js" -o -name "*.css" -o -name "*.txt  " \) -exec chmod 644 {} \;
chmod 755 $(grep -RH '/usr/bin/' %{buildroot}%{_datadir}/%{name} | cut -d: -f1)

# Create a sysusers.d config file
cat >%{name}.sysusers.conf <<EOF
u %{name} - 'SABnzbd' %{_sharedstatedir}/%{name} -
EOF

install -m0644 -D %{name}.sysusers.conf %{buildroot}%{_sysusersdir}/%{name}.conf

%find_lang SABnzbd

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
%{_sysconfdir}/bash_completion.d/sabnzbd
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service
%attr(750,%{user},%{group}) %{_localstatedir}/log/%{name}

%changelog
* Fri Jul 03 2026 Simone Caronni <negativo17@gmail.com> - 5.0.4-1
- Update to 5.0.4.

* Mon May 18 2026 Simone Caronni <negativo17@gmail.com> - 5.0.3-1
- Update to 5.0.3.

* Sun May 10 2026 Simone Caronni <negativo17@gmail.com> - 5.0.1-1
- Update to 5.0.1.

* Mon Apr 27 2026 Simone Caronni <negativo17@gmail.com> - 4.5.5-2
- Require python3-rarfile.

* Thu Nov 20 2025 Simone Caronni <negativo17@gmail.com> - 4.5.5-1
- Update to 4.5.5.
- Switch to sysusers.d mechanism.

* Tue Sep 02 2025 Simone Caronni <negativo17@gmail.com> - 4.5.3-1
- Update to 4.5.3.

* Fri Aug 01 2025 Simone Caronni <negativo17@gmail.com> - 4.5.2-1
- Update to 4.5.2.

* Wed Apr 16 2025 Simone Caronni <negativo17@gmail.com> - 4.5.1-1
- Update to 4.5.1.

* Fri Dec 27 2024 Simone Caronni <negativo17@gmail.com> - 4.4.1-1
- Update to 4.4.1.

* Fri Dec 13 2024 Simone Caronni <negativo17@gmail.com> - 4.4.0-1
- Update to 4.4.0.

* Sun Aug 25 2024 Simone Caronni <negativo17@gmail.com> - 4.3.3-1
- Update to 4.3.3.

* Fri Jun 28 2024 Simone Caronni <negativo17@gmail.com> - 4.3.2-2
- Drop Appstream metadata.

* Mon Jun 24 2024 Simone Caronni <negativo17@gmail.com> - 4.3.2-1
- Update to 4.3.2.

* Mon Jun 24 2024 Simone Caronni <negativo17@gmail.com> - 4.3.1-2
- Use python automatic requirements.

* Mon May 13 2024 Simone Caronni <negativo17@gmail.com> - 4.3.1-1
- Update to 4.3.1.

* Tue Mar 12 2024 Simone Caronni <negativo17@gmail.com> - 4.2.3-1
- Update to 4.2.3.

* Thu Feb 22 2024 Simone Caronni <negativo17@gmail.com> - 4.2.2-2
- Update requirements.

* Wed Jan 31 2024 Simone Caronni <negativo17@gmail.com> - 4.2.2-1
- Update to 4.2.2.

* Sat Jan 06 2024 Simone Caronni <negativo17@gmail.com> - 4.2.1-1
- Update to 4.2.1.

* Sat Jan 06 2024 Simone Caronni <negativo17@gmail.com> - 4.2.0-1
- Update to 4.2.0.

* Sat Nov 11 2023 Simone Caronni <negativo17@gmail.com> - 4.1.0-2
- Adjust requirements.

* Fri Nov 10 2023 Simone Caronni <negativo17@gmail.com> - 4.1.0-1
- Update to 4.1.0.

* Fri Nov 10 2023 Simone Caronni <negativo17@gmail.com> - 4.0.3-2
- Adjust requirements.

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
