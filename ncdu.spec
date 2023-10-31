Summary:	Text-based disk usage viewer
Name:		ncdu
Version:	1.19
Release:	1
License:	MIT
Group:		Applications/File
URL:		http://dev.yorhel.nl/ncdu/
Source0:	http://dev.yorhel.nl/download/%{name}-%{version}.tar.gz
# Source0-md5:	7986451d5b222b8a99b5382f33a30831
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
%doc README
%attr(755,root,root) %{_bindir}/ncdu
%{_mandir}/man1/ncdu.1*
