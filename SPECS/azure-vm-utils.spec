Name:           azure-vm-utils
Version:        0.7.0
Release:        1%{?dist}
Summary:        Core utilities and configuration for Linux VMs on Azure

License:        MIT
URL:            https://github.com/Azure/%{name}
Source:         %{url}/archive/v%{version}/%{name}-v%{version}.tar.gz

# It only supports x86_64 and aarch64 on Azure currently
ExclusiveArch:    x86_64 aarch64

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  pkgconfig(libudev)
BuildRequires:  json-c-devel
BuildRequires:  libcmocka-devel
BuildRequires:  systemd-rpm-macros
Requires:       util-linux
Recommends:     mdadm
Conflicts:      WALinuxAgent-udev < 2.14.0.1-2

Provides:       azure-nvme-utils = %{version}-%{release}
Obsoletes:      azure-nvme-utils < 0.1.3-3

%description
This package provides a home for core utilities, udev rules and other
configuration to support Linux VMs on Azure.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake -DVERSION="%{version}-%{release}" -DAZURE_NVME_ID_INSTALL_DIR="%{_bindir}"
%cmake_build

%install
%cmake_install
install -D -m 0755 initramfs/dracut/modules.d/97azure-disk/module-setup.sh %{buildroot}%{_prefix}/lib/dracut/modules.d/97azure-disk/module-setup.sh
install -D -m 0755 initramfs/dracut/modules.d/97azure-unmanaged-sriov/module-setup.sh %{buildroot}%{_prefix}/lib/dracut/modules.d/97azure-unmanaged-sriov/module-setup.sh
rm %{buildroot}%{_bindir}/azure-vm-utils-selftest
rm %{buildroot}%{_mandir}/man8/azure-vm-utils-selftest.8

%check
%ctest

%files
%defattr(-,root,root,-)
%dir %{_prefix}/lib/dracut/modules.d/97azure-disk
%{_prefix}/lib/dracut/modules.d/97azure-disk/module-setup.sh
%{_prefix}/lib/dracut/modules.d/97azure-unmanaged-sriov/module-setup.sh
%{_prefix}/lib/systemd/network/01-azure-unmanaged-sriov.network
%{_unitdir}/azure-ephemeral-disk-setup.service
%{_udevrulesdir}/10-azure-unmanaged-sriov.rules
%{_udevrulesdir}/80-azure-disk.rules
%{_bindir}/azure-ephemeral-disk-setup
%{_bindir}/azure-nvme-id
%{_mandir}/man8/azure-ephemeral-disk-setup.8.*
%{_mandir}/man8/azure-nvme-id.8.*
%config(noreplace) %{_sysconfdir}/azure-ephemeral-disk-setup.conf

%changelog
* Tue Oct 28 2025 Vinay Mulugund <vmulugun@redhat.com> - 0.7.0-1
- Rebase to 0.7.0 [RHEL-99446]
- Resolves: RHEL-99446
  ([Azure][rhel-9] azure-vm-utils rebase)

* Thu May 8 2025 Huijuan Zhao <huzhao@redhat.com> - 0.5.2-1
- Initial commit on c19s
