%define		module		awscli
%define		egg_name	awscli
%define		pypi_name	awscli
Summary:	Universal Command Line Environment for AWS
Summary(pl.UTF-8):	Uniwersalne środowisko linii polecen dla AWS
Name:		awscli
Version:	1.33.34
Release:	3
License:	ASL 2.0 and MIT
Group:		Applications/Networking
Source0:	https://files.pythonhosted.org/packages/source/a/awscli/%{name}-%{version}.tar.gz
# Source0-md5:	48d39c6a5f150bb4dc4d8556ff9114da
Patch0:		%{name}-relax_deps.patch
URL:		https://aws.amazon.com/cli/
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.719
Requires:	python3-%{pypi_name} = %{version}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package provides a unified command line interface to Amazon Web
Services.

%description -l pl.UTF-8
Ten pakiet dostarcza ujednolicony interfejs linii poleceń do usług
Amazon Web Services.

%package -n python3-%{pypi_name}
Summary:	Python 3 package for awscli
Summary(pl.UTF-8):	Pakiet Pythona 3 do awscli
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.8
Obsoletes:	python-awscli < 1.20.40

%description -n python3-%{pypi_name}
Python 3 package for awscli.

%description -n python3-%{pypi_name} -l pl.UTF-8
Pakiet Pythona 3 do awscli.

%prep
%setup -q
%patch -P 0 -p1

%{__rm} -r %{name}.egg-info

%build
%py3_build

%install
rm -rf $RPM_BUILD_ROOT
%py3_install

# We don't need the Windows CMD script
%{__rm} $RPM_BUILD_ROOT%{_bindir}/aws.cmd

# Fix path and permissions for bash completion
install -d $RPM_BUILD_ROOT%{bash_compdir}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/aws_bash_completer $RPM_BUILD_ROOT%{bash_compdir}
# Fix path and permissions for zsh completion
install -d $RPM_BUILD_ROOT%{zsh_compdir}
%{__mv} $RPM_BUILD_ROOT%{_bindir}/aws_zsh_completer.sh $RPM_BUILD_ROOT%{zsh_compdir}

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
