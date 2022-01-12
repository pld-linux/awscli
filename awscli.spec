%define		module		awscli
%define		egg_name	awscli
%define		pypi_name	awscli
Summary:	Universal Command Line Environment for AWS
Name:		awscli
Version:	1.22.33
Release:	1
License:	ASL 2.0 and MIT
Group:		Applications/Networking
Source0:	https://files.pythonhosted.org/packages/source/a/awscli/%{name}-%{version}.tar.gz
# Source0-md5:	441cf1b967b71ed5723b5e6cd99cc2c2
Patch0:		%{name}-relax_deps.patch
URL:		https://aws.amazon.com/cli/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.719
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools
Requires:	python3-%{pypi_name} = %{version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a unified command line interface to Amazon Web
Services.

%package -n python3-%{pypi_name}
Summary:	Python 3 package for awscli
Group:		Libraries/Python
Requires:	python3-PyYAML >= 3.10
Requires:	python3-botocore >= 1.23.33
Requires:	python3-colorama >= 0.2.5
Requires:	python3-docutils >= 0.10
Requires:	python3-modules >= 1:3.6
Requires:	python3-rsa >= 3.1.2
Requires:	python3-s3transfer >= 0.5
Obsoletes:	python-awscli < 1.20.40

%description -n python3-%{pypi_name}
Python 3 package for awscli.

%prep
%setup -q
%patch0 -p1

rm -r %{name}.egg-info

%build
%py3_build

%install
rm -rf $RPM_BUILD_ROOT
%py3_install

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

%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
