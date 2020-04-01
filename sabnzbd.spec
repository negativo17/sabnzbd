%global user %{name}
%global group %{name}
%global __python %{__python2}

Name:           sabnzbd
Version:        2.3.9
Release:        2%{?dist}
Summary:        A Python based monitoring and tracking tool for Plex Media Server
License:        GPLv2+
URL:            https://sabnzbd.org/
BuildArch:      noarch

Source0:        https://github.com/%{name}/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        config.ini
Source10:       %{name}.service
Source11:       %{name}.xml

BuildRequires:  firewalld-filesystem
BuildRequires:  systemd
BuildRequires:  tar

Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem
Requires:       par2cmdline
Requires:       python2
Requires:       python2-sabyenc >= 3.3.5
Requires:       rar
Requires(pre):  shadow-utils

%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:       python2-cheetah
Requires:       python2-six
%else
Requires:       python-cheetah
Requires:       python-six
Requires:       python-yenc
%endif

%description
A python based web application for monitoring, analytics and notifications for
Plex Media Server.

%prep
%autosetup -n %{name}-%{version}

%install

mkdir -p %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{_prefix}/lib/firewalld/services/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}

cp -fr SABnzbd.py cherrypy util sabnzbd po interfaces icons gntp email %{buildroot}%{_datadir}/%{name}

install -m 0644 -p %{SOURCE1} %{buildroot}%{_sysconfdir}/%{name}/config.ini

install -m 0644 -p %{SOURCE10} %{buildroot}%{_unitdir}/%{name}.service
install -m 0644 -p %{SOURCE11} %{buildroot}%{_prefix}/lib/firewalld/services/%{name}.xml

# Always invoke Python 2
find %{buildroot} \( -name "*.py" -o -name "cherryd" \) -exec sed -i \
    -e 's|/usr/bin/env python|/usr/bin/env python2|g' \
    -e 's|/usr/bin/python|/usr/bin/env python2|g' {} \;

find %{buildroot} \( -name "*.js" -o -name "*.css" \) -exec chmod 644 {} \;

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

%files
%license LICENSE.txt
%doc README.md README.mkd ABOUT.txt
%attr(750,%{user},%{group}) %{_sharedstatedir}/%{name}
%attr(750,%{user},%{group}) %{_sysconfdir}/%{name}
%config(noreplace) %attr(644,%{user},%{group}) %{_sysconfdir}/%{name}/config.ini
%{_datadir}/%{name}
%{_prefix}/lib/firewalld/services/%{name}.xml
%{_unitdir}/%{name}.service
%attr(750,%{user},%{group}) %{_localstatedir}/log/%{name}

%changelog
* Sun Dec 01 2019 Simone Caronni <negativo17@gmail.com> - 2.3.9-2
- Add default configuration file.

* Sun Nov 17 2019 Simone Caronni <negativo17@gmail.com> - 2.3.9-1
- First build.
