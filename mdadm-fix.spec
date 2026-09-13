Name:           mdadm
Version:        4.4
Release:        4.1%{?dist}
Summary:        mdadm 4.4 with fix for missing sysfs module parameter on pre-5.18 kernels

License:        GPL-2.0-or-later
URL:            https://github.com/SisyphusAeolides/mdadm-fix

# Get original mdadm source from upstream
Source0:        https://git.kernel.org/pub/scm/utils/mdadm/mdadm.git/snapshot/mdadm-4.4.tar.gz
Patch0:         0044-mdadm-skip-missing-legacy_async-del-gendisk.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  systemd-devel

Provides:       mdadm = %{version}-%{release}

%description
mdadm is a tool for managing Linux Software RAID arrays. This package
includes the upstream 4.4 release plus a fix that eliminates a hard
failure on kernels older than 5.18 that lack the
legacy_async_del_gendisk sysfs parameter.

%prep
%autosetup -n mdadm-4.4 -p1

%build
%make_build

%install
%make_install INSTALL=install
install -Dm644 mdadm.conf.5 %{buildroot}%{_mandir}/man5/mdadm.conf.5

%files
%license COPYING
%doc README.md
%{_sbindir}/mdadm
%{_sbindir}/mdmon
%{_mandir}/man5/mdadm.conf.5*
%{_mandir}/man8/mdadm.8*
%{_mandir}/man8/mdmon.8*

%changelog
* Sun Sep 13 2026 Kenny Glauner <SisyphusAeolides@pm.me> - 4.4-4.1
- Apply fix for missing legacy_async_del_gendisk sysfs parameter on pre-5.18 kernels
- Eliminate TOCTOU access(F_OK) pre-check; use errno discrimination on open(2) directly
