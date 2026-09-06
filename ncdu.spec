Summary:	Text-based disk usage viewer
Name:		ncdu
Version:	1.23.0
Release:	1
License:	MIT
Group:		Applications/File
# Maintenance fork; the original author died and dev.yorhel.nl is frozen at 1.22.
URL:		https://github.com/BratishkaErik/ncdu
Source0:	https://github.com/BratishkaErik/ncdu/releases/download/v%{version}/%{name}-%{version}-src.tar.gz
# Source0-md5:	382be8498c62158a6f1c3848be3764ff
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ncurses-devel
BuildRequires:	pkgconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ncdu (NCurses Disk Usage) is a curses-based version of the well-known
'du', and provides a fast way to see what directories are using your
disk space.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/ncdu
%{_mandir}/man1/ncdu.1*
