# Package namespaces
%global ns_name ea
%global ns_dir /opt/cpanel
%global _scl_prefix %ns_dir

# Let's have a fallback, in case we're not called quite correctly.
%{!?scl:%{expand:
%global scl_name_base %{ns_name}-php
%global scl_name_version 56
%global scl %{scl_name_base}%{scl_name_version}
}}

%scl_package %scl

# Starting with PHP 5.6, the IonCube loader needs to be loaded first
%if "%{php_version}" < "5.6"
%global inifile ioncube.ini
%else
%global inifile 01-ioncube.ini
%endif

Name:    %{?scl_prefix}php-ioncube
Vendor:  ionCube Ltd.
Summary: Loader for ionCube-encoded PHP files
Version: 4.7.5
Release: 1%{?dist}
License: Redistributable
Group:   Development/Languages
URL:     http://www.ioncube.com/loaders.php

# We'll only do 64-bit packages, so no need for 32-bit libraries.  The
# archive contains the license file, so no need to have it as a
# separate source file.
Source: http://downloads3.ioncube.com/loader_downloads/ioncube_loaders_lin_x86-64.tar.gz

BuildRequires: scl-utils-build
BuildRequires: %{?scl_prefix}scldevel
BuildRequires: %{?scl_prefix}build
BuildRequires: %{?scl_prefix}php-devel
Requires:      %{?scl_prefix}php(zend-abi) = %{php_zend_api}
Requires:      %{?scl_prefix}php(api) = %{php_core_api}

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
* Mon Jul 06 2015 Trinity Quirk <trinity.quirk@cpanel.net> - 4.7.5-1
- Initial creation
