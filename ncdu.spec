%define	gitref	224d40845c9b39bba4efcf3c57bd913fed2f21a4
%define	snap	20260822
%define	rev_translate_c	0944784e197e419433a21d4b28bfc65e48e7d514
%define	rev_aro		8d5f79925cfd60d1c894b478b3502ed1e376e9ba
# zig resolves --system packages by directory name, which must be the .hash from
# the manifest requiring them: ncdu's build.zig.zon for translate_c, translate-c's
# own for aro. Re-read both after moving either revision above.
%define	hash_translate_c	translate_c-0.0.0-Q_BUWo5NBwBs3K0a-B1XbxEF3gFdTb75VgOE0FL-2qKL
%define	hash_aro		aro-0.0.0-JSD1QhdtNwC3tSPo_L0O9EOdOqEXYxE5tOrih2p4RGKx
#
Summary:	Text-based disk usage viewer
Summary(pl.UTF-8):	Tekstowa przeglądarka wykorzystania miejsca na dysku
Name:		ncdu
Version:	2.11.1
Release:	0.%{snap}.1
License:	MIT
Group:		Applications/File
# Maintenance fork; the original author died and dev.yorhel.nl is frozen at 2.9.2.
# Packaged off the zig-0.17 branch because the 2.11.1 tag still targets zig 0.16.
URL:		https://github.com/BratishkaErik/ncdu
Source0:	https://github.com/BratishkaErik/ncdu/archive/%{gitref}/%{name}-%{snap}.tar.gz
# Source0-md5:	8f6429edb63dd2d25077be87d1663c45
# Zig dependencies; the build has no network, so they are unpacked into a
# --system package directory in %%prep. aro is a git+ dependency of translate-c,
# but zig hashes tree content, so a commit archive is equivalent.
Source1:	https://codeberg.org/ziglang/translate-c/archive/%{rev_translate_c}.tar.gz
# Source1-md5:	28d0d131b933752d6bf7ce37150503e2
Source2:	https://codeberg.org/ziglang/arocc/archive/%{rev_aro}.tar.gz
# Source2-md5:	1e9440e3aa0d2085cabab614adaa6da4
# translate-c pinned by the branch predates the zig snapshot PLD ships; aro then
# fails on std.ArrayList gaining pointer_stability.
Patch0:		%{name}-translate-c.patch
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
%setup -q -n %{name}-%{gitref}
%patch -P0 -p1

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
