# TODO: system MathMLSolver? https://sourceforge.net/projects/mathmlsolver/files/
#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	3DS Max / Maya scenes exporter to COLLADA format
Summary(pl.UTF-8):	Biblioteki do eksportu scen 3DS Max / Maya do formatu COLLADA
Name:		OpenCOLLADA
Version:	1.6.68
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/KhronosGroup/OpenCOLLADA/releases
Source0:	https://github.com/KhronosGroup/OpenCOLLADA/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ee7dae874019fea7be11613d07567493
Patch0:		%{name}-pcre.patch
Patch1:		%{name}-system-zlib.patch
Patch2:		%{name}-install-paths.patch
URL:		http://www.opencollada.org/
BuildRequires:	cmake >= 2.6
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libxml2-devel >= 2
BuildRequires:	pcre-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
COLLADAMax and COLLADAMaya are new implementation of a 3ds Max or Maya
plug-ins to export scene or parts of it to a COLLADA file, released
under an MIT-license. 

%description -l pl.UTF-8
COLLADAMax i COLLADAMaya to nowa implementacja wtyczek 3ds Max i Maya
do eksportu scen lub ich części do plików COLLADA - wydana na licencji
MIT.

%package devel
Summary:	Header files for OpenCOLLADA libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek OpenCOLLADA
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenCOLLADA libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek OpenCOLLADA.

%package static
Summary:	Static OpenCOLLADA libraries
Summary(pl.UTF-8):	Statyczne biblioteki OpenCOLLADA
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenCOLLADA libraries.

%description static -l pl.UTF-8
Statyczne biblioteki OpenCOLLADA.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
install -d build
cd build
%cmake .. \
	-DOPENCOLLADA_INST_CMAKECONFIG=%{_libdir}/cmake/opencollada \
	-DOPENCOLLADA_INST_LIBRARY=%{_libdir} \
	-DUSE_SHARED=ON \
	%{!?with_static_libs:-DUSE_STATIC=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_libdir}/libGeneratedSaxParser.so
%attr(755,root,root) %{_libdir}/libMathMLSolver.so
%attr(755,root,root) %{_libdir}/libOpenCOLLADABaseUtils.so
%attr(755,root,root) %{_libdir}/libOpenCOLLADAFramework.so
%attr(755,root,root) %{_libdir}/libOpenCOLLADASaxFrameworkLoader.so
%attr(755,root,root) %{_libdir}/libOpenCOLLADAStreamWriter.so
%attr(755,root,root) %{_libdir}/libUTF.so
%attr(755,root,root) %{_libdir}/libbuffer.so
%attr(755,root,root) %{_libdir}/libftoa.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/opencollada
%{_libdir}/cmake/opencollada

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libGeneratedSaxParser.a
%{_libdir}/libMathMLSolver.a
%{_libdir}/libOpenCOLLADABaseUtils.a
%{_libdir}/libOpenCOLLADAFramework.a
%{_libdir}/libOpenCOLLADASaxFrameworkLoader.a
%{_libdir}/libOpenCOLLADAStreamWriter.a
%{_libdir}/libUTF.a
%{_libdir}/libbuffer.a
%{_libdir}/libftoa.a
%endif
