#
# Conditional build:
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		awscli
%define		egg_name	awscli
%define		pypi_name	awscli
Summary:	Universal Command Line Environment for AWS
Name:		awscli
Version:	1.15.72
Release:	1
License:	ASL 2.0 and MIT
Group:		Applications/Networking
Source0:	https://files.pythonhosted.org/packages/source/a/awscli/%{name}-%{version}.tar.gz
# Source0-md5:	11f6e8522fb2771b67cd150b3e891e03
URL:		https://aws.amazon.com/cli/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.719
%if %{with python2}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
%if %{with python3}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a unified command line interface to Amazon Web
Services.

%package -n python-%{pypi_name}
Summary:	Python 2 package for awscli
Group:		Libraries/Python
Requires:	python-PyYAML >= 3.10
Requires:	python-botocore >= 1.10.42
Requires:	python-colorama >= 0.2.5
Requires:	python-docutils >= 0.10
Requires:	python-modules
Requires:	python-rsa >= 3.1.2
Requires:	python-s3transfer >= 0.1.9

%description -n python-%{pypi_name}
Python 2 package for awscli.

%package -n python3-%{pypi_name}
Summary:	Python 3 package for awscli
Group:		Libraries/Python
Requires:	python3-PyYAML >= 3.10
Requires:	python3-botocore >= 1.10.42
Requires:	python3-colorama >= 0.2.5
Requires:	python3-docutils >= 0.10
Requires:	python3-modules
Requires:	python3-rsa >= 3.1.2
Requires:	python3-s3transfer >= 0.1.9

%description -n python3-%{pypi_name}
Python 3 package for awscli.

%prep
%setup -q

rm -r %{name}.egg-info

%build
%if %{with python3}
%py_build
%endif
%if %{with python3}
%py3_build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif
%if %{with python3}
%py3_install
%endif

# We don't need the Windows CMD script
rm $RPM_BUILD_ROOT%{_bindir}/aws.cmd

# Fix path and permissions for bash completition
install -d $RPM_BUILD_ROOT%{bash_compdir}
mv $RPM_BUILD_ROOT%{_bindir}/aws_bash_completer $RPM_BUILD_ROOT%{bash_compdir}
# Fix path and permissions for zsh completition
install -d $RPM_BUILD_ROOT%{zsh_compdir}
mv $RPM_BUILD_ROOT%{_bindir}/aws_zsh_completer.sh $RPM_BUILD_ROOT%{zsh_compdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE.txt
%attr(755,root,root) %{_bindir}/aws
%attr(755,root,root) %{_bindir}/aws_completer
%{bash_compdir}/aws_bash_completer
%{zsh_compdir}/aws_zsh_completer.sh

%if %{with python2}
%files -n python-%{pypi_name}
%defattr(644,root,root,755)
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif
