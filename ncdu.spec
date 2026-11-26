%define	rev_aro		630d99ed60fe61ccabe721f1af60881f8b2adde3
# zig resolves --system packages by directory name, which must be the .hash from
# the manifest requiring them: ncdu's build.zig.zon for translate_c, translate-c's
# own for aro. Re-read both after moving either version above.
%define	ver_translate_c	2.0.2
%define	hash_translate_c	translate_c-2.0.2-Q_BUWvBNBwBgPKQJPblip6M7AHNK_IPNPmyv4rSIQMQc
%define	hash_aro		aro-0.0.0-JSD1QvCRNwC2O1Jkop9TO6sXb1U1vhrH8FnYK1VdEMKn
#
Summary:	Text-based disk usage viewer
Summary(pl.UTF-8):	Tekstowa przeglądarka wykorzystania miejsca na dysku
Name:		ncdu
Version:	2.13.0
Release:	1
License:	MIT
Group:		Applications/File
# Maintenance fork; the original author died and dev.yorhel.nl is frozen at 2.9.2.
URL:		https://github.com/BratishkaErik/ncdu
Source0:	https://github.com/BratishkaErik/ncdu/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ff5ffbbbbffc5ecbfbfa9f984d0dac25
# Zig dependencies; the build has no network, so they are unpacked into a
# --system package directory in %%prep. aro is a git+ dependency of translate-c,
# but zig hashes tree content, so a commit archive is equivalent.
Source1:	https://codeberg.org/ziglang/translate-c/archive/%{ver_translate_c}.tar.gz
# Source1-md5:	e0fbf2ed1cee7214929da13886967d32
Source2:	https://codeberg.org/ziglang/arocc/archive/%{rev_aro}.tar.gz
# Source2-md5:	b7a92d68ad84331cc36f5a476fc494e5
BuildRequires:	ncurses-devel
BuildRequires:	zig
BuildRequires:	zstd-devel
# written in zig, which PLD can only build on x86_64
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ncdu (NCurses Disk Usage) is a curses-based version of the well-known
'du', and provides a fast way to see what directories are using your
disk space.

%description -l pl.UTF-8
ncdu (NCurses Disk Usage) to oparta na bibliotece curses odmiana dobrze
znanego polecenia 'du', pozwalająca szybko sprawdzić, które katalogi
zajmują miejsce na dysku.

%prep
%setup -q

install -d zig-pkg/%{hash_translate_c} zig-pkg/%{hash_aro}
tar xf %{SOURCE1} -C zig-pkg/%{hash_translate_c} --strip-components=1
tar xf %{SOURCE2} -C zig-pkg/%{hash_aro} --strip-components=1

%build
export ZIG_GLOBAL_CACHE_DIR=$(pwd)/.zig-cache
export ZIG_LOCAL_CACHE_DIR=$(pwd)/.zig-cache
zig build \
	--system zig-pkg \
	--prefix $(pwd)/out \
	--build-id=sha1 \
	-Dcpu=baseline \
	-Doptimize=ReleaseFast \
	-Dpie \
	-fsys=ncurses \
	-fsys=zstd

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_mandir}/man1
install -p out/bin/ncdu $RPM_BUILD_ROOT%{_bindir}
cp -p ncdu.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog README.md
%attr(755,root,root) %{_bindir}/ncdu
%{_mandir}/man1/ncdu.1*
