#
# Conditional build:
%bcond_without	tests	# unit tests

%define		module	pysnmp
Summary:	SNMP engine for Python
Summary(pl.UTF-8):	Obsługa SNMP dla Pythona
Name:		python3-%{module}
Version:	7.1.30
Release:	1
License:	BSD
Group:		Libraries/Python
# PyPI sdist lacks tests and examples
Source0:	https://github.com/lextudio/pysnmp/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	362fa55079441d9160d28a545945192e
URL:		https://www.pysnmp.com/
BuildRequires:	python3 >= 1:3.10
BuildRequires:	python3-build
BuildRequires:	python3-flit_core >= 3.9.0
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.10
%if %{with tests}
BuildRequires:	mibs-net-snmp
BuildRequires:	python3-cryptography
BuildRequires:	python3-pyasn1 >= 0.6.4
BuildRequires:	python3-pysmi >= 2.0.0
BuildRequires:	python3-pytest >= 7.2.0
BuildRequires:	python3-pytest-asyncio >= 0.21.1
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
Requires:	python3-modules >= 1:3.10
# DES/3DES/AES privacy for SNMPv3 USM; imported lazily, so not autodetected
Requires:	python3-cryptography
Suggests:	python3-pysmi
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a set of tools required by the Structure of Management
Information (SMI v.1 & v.2) to be used in Python programming
environment. Primarily, they are SNMP engine and MIB compiler.

%description -l pl.UTF-8
Zestaw narzędzi pozwalających pisać w Pythonie programy korzystające z
protokołu SNMP. Zawiera procedury służące do zarządzania obiektami MIB
(Management Information Base), opisanych przez normy SMI (Structure of
Management Information) v1 i v2.

%package examples
Summary:	Example programs for Python pysnmp module
Summary(pl.UTF-8):	Programy przykładowe do modułu Pythona pysnmp
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description examples
This package contains example programs for Python pysnmp module.

%description examples -l pl.UTF-8
Ten pakiet zawiera przykładowe programy do modułu Pythona pysnmp.

%prep
%setup -q -n %{module}-%{version}

%build
%py3_build_pyproject

%if %{with tests}
# skipped: need demo.pysnmp.com, LEXTUDIO-TEST-MIB from mibs.pysnmp.com,
# "localhost" resolving to ::1, or CISCO MIBs precompiled into ~/.pysnmp/mibs;
# --deselect matches by nodeid prefix
# MIB compiler writes into ~/.pysnmp/mibs
HOME=$(pwd)/test-home \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_asyncio.plugin \
%{__python3} -m pytest tests \
	--ignore=tests/smi/manager/test_mib-tree-inspection.py \
	--deselect tests/hlapi/v1arch/asyncio/manager/cmdgen/test_v1arch_v1_get.py::test_v1_get_ipv6 \
	--deselect tests/hlapi/v1arch/asyncio/manager/cmdgen/test_v1arch_v1_get.py::test_v1_get_dateandtime_object \
	--deselect tests/hlapi/v1arch/asyncio/manager/cmdgen/test_v1arch_v1_get.py::test_v1_get_physaddress_object \
	--deselect tests/hlapi/v1arch/asyncio/manager/cmdgen/test_v1arch_v1_get.py::test_v1_get_scaled_integer_object \
	--deselect tests/hlapi/v1arch/asyncio/manager/cmdgen/test_v1arch_v1_get.py::test_v1_get_scaled_unsigned_object \
	--deselect tests/hlapi/v1arch/asyncio/manager/cmdgen/test_v1arch_v1_get.py::test_v1_get_multiple_objects \
	--deselect tests/hlapi/v1arch/asyncio/manager/cmdgen/test_v1arch_v1_set.py::test_v1_set_mac_address \
	--deselect tests/hlapi/v1arch/asyncio/manager/cmdgen/test_v1arch_v2c_bulk.py::test_v2c_bulk_multiple_input \
	--deselect tests/hlapi/v1arch/asyncio/manager/cmdgen/test_v1arch_v2c_bulkwalk.py::test_v2c_get_table_bulk \
	--deselect tests/hlapi/v3arch/asyncio/manager/cmdgen/test_v1_get.py::test_v1_get_ipv6 \
	--deselect tests/hlapi/v3arch/asyncio/manager/cmdgen/test_v2c_bulkwalk.py::test_v2c_get_table_bulk \
	--deselect tests/smi/manager/test_configure-mib-viewer-and-resolve-pdu-varbinds.py::test_syntax_integer \
	--deselect tests/smi/manager/test_configure-mib-viewer-and-resolve-pdu-varbinds.py::test_syntax_unsigned \
	--deselect tests/smi/manager/test_configure-mib-viewer-and-resolve-pdu-varbinds.py::test_syntax_fixed_length_octet_string
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}

%py3_install_pyproject

cp -a examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE.rst README.md SECURITY.md THANKS.txt TODO.txt
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{module}-%{version}.dist-info

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}
