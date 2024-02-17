Name:           inotify-tools
Version:        3.22.6.0
Release:        0
Summary:        Command line utilities for inotify

Group:          Applications/System
License:        GPLv2
URL:            https://github.com/inotify-tools/inotify-tools
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  autoconf

%description
inotify-tools is a set of command-line programs for Linux providing
a simple interface to inotify. These programs can be used to monitor
and act upon filesystem events.

%if "%{?vendor}" == "chum"
Title: inotify-tools
PackagedBy: nephros
Type: console-application
Categories:
  - System
  - Utility
Custom:
  Repo:          https://github.com/inotify-tools/inotify-tools
  PackagingRepo: https://github.com/sailfishos-chum/inotify-tools
%endif

%package        devel
Summary:        Headers and libraries for building apps that use libinotifytools
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains headers and libraries required to build applications
that use the libinotifytools library.

%prep
%setup -q -n %{name}-%{version}/upstream

%build
%reconfigure \
        --disable-dependency-tracking \
        --disable-static \
        --disable-doxygen \
        CFLAGS="$RPM_OPT_FLAGS -fPIC -pie" \
        CXXFLAGS="$RPM_OPT_FLAGS -fPIC -pie"
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
rm -rf %{buildroot}/%{_docdir}
rm -rf %{buildroot}/%{_mandir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%license COPYING
%doc README.md
%{_bindir}/inotifywait
%{_bindir}/inotifywatch
%{_libdir}/libinotifytools.so.*

%files devel
%defattr(-,root,root,-)
%doc AUTHORS NEWS
%dir %{_includedir}/inotifytools/
%{_includedir}/inotifytools/*.h
%{_libdir}/libinotifytools.so

