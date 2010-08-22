Summary:	Text-based disk usage viewer
Name:		ncdu
Version:	1.6
Release:	1
License:	MIT
Group:		Applications/File
URL:		http://dev.yorhel.nl/ncdu/
Source0:	http://dev.yorhel.nl/download/%{name}-%{version}.tar.gz
Patch0:		ncurses-lib.patch
# Source0-md5:	95d29cf64af2d8cf4b5005e6e3d60384
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ncdu (NCurses Disk Usage) is a curses-based version of the well-known
'du', and provides a fast way to see what directories are using your
disk space.

%prep
%setup -q
%patch0 -p1

%build
CPPFLAGS="-I/usr/include/ncurses"
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
%doc AUTHORS ChangeLog TODO
%attr(755,root,root) %{_bindir}/ncdu
%{_mandir}/man1/ncdu.1*
