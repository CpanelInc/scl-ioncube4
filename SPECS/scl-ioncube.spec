%define debug_package %{nil}

%global extension_type php
%global upstream_name ioncube

%{?scl:%global _scl_prefix /opt/cpanel}
%{?scl:%scl_package %{extension_type}-%{upstream_name}}
%{?scl:BuildRequires: scl-utils-build}
%{?scl:Requires: %scl_runtime}
%{!?scl:%global pkg_name %{name}}

# must redefine this in the spec file because OBS doesn't know how
# to handle macros in BuildRequires statements
%{?scl:%global scl_prefix %{scl}-}

# Use this to get access to %{php_version} macro
%scl_package_override

# OBS builds the 32-bit targets as arch 'i586', and more typical
# 32-bit architecture is 'i386', but 32-bit archive is named 'x86'.
# 64-bit archive is 'x86-64', rather than 'x86_64'.
%if "%{_arch}" == "i586" || "%{_arch}" == "i386"
%global archive_arch x86
%else
%if "%{_arch}" == "x86_64"
%global archive_arch x86-64
%else
%global archive_arch %{_arch}
%endif
%endif

# Starting with PHP 5.6, the IonCube loader needs to be loaded first
%if "%{php_version}" < "5.6"
%global inifile ioncube.ini
%else
%global inifile 01-ioncube.ini
%endif

Name:    %{?scl_prefix}%{extension_type}-%{upstream_name}
Vendor:  ionCube Ltd.
Summary: Loader for ionCube-encoded PHP files
Version: 4.7.5
Release: 5%{?dist}
License: Redistributable
Group:   Development/Languages
URL:     http://www.ioncube.com/loaders.php
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# There is a different distribution archive per architecture.  The
# archive contains the license file, so no need to have it as a
# separate source file.
Source: http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_%{archive_arch}.tar.gz

BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}
Conflicts:     %{?scl_prefix}php-ioncube5

# Don't provide extensions as shared library resources
%{?filter_provides_in: %filter_provides_in %{php_extdir}/.*\.so$}
%{?filter_setup}

%description
The ionCube Loader enables use of ionCube-encoded PHP files running
under PHP %{php_version}.

%prep
%setup -q -n ioncube

%build
# Nothing to do here, since it's a binary distribution.

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

# The module itself
install -d -m 755 $RPM_BUILD_ROOT%{php_extdir}
install -m 755 ioncube_loader_lin_%{php_version}.so $RPM_BUILD_ROOT%{php_extdir}

# The ini snippet
install -d -m 755 $RPM_BUILD_ROOT%{php_inidir}
cat > $RPM_BUILD_ROOT%{php_inidir}/%{inifile} <<EOF
; Enable IonCube Loader extension module
zend_extension="%{php_extdir}/ioncube_loader_lin_%{php_version}.so"
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.txt
%config(noreplace) %{php_inidir}/%{inifile}
%{php_extdir}/ioncube_loader_lin_%{php_version}.so

%changelog
* Thu Mar 24 2016 S. Kurt Newman <kurt.newman@cpanel.net> - 4.7.5-5
- Added scl_package_override macro to regain access to global
  PHP macros that contain location and verison information.

* Wed Mar 23 2016 Dan Muey <dan@cpanel.net> - 4.7.5-4
- Add conflict for ioncube v5 in same PHP version

* Wed Mar 09 2016 S. Kurt Newman <kurt.newman@cpanel.net> - 4.7.5-3
- Resolve internal SCL builds optimizations with Makefiles (EA-4259)

* Mon Jul 06 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 4.7.5-1
- Initial creation
