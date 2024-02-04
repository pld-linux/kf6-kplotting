#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.249.0
%define		qtver		5.15.2
%define		kfname		kplotting
#
Summary:	Data plotting
Name:		kf6-%{kfname}
Version:	5.249.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	ba5bd1f6950a2f0d33bb04598ac12592
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel
BuildRequires:	Qt6Gui-devel >= 5.3.1
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	kf6-dirs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KPlotWidget is a QWidget-derived class that provides a virtual base
class for easy data-plotting. The idea behind KPlotWidget is that you
only have to specify information in "data units"; i.e., the natural
units of the data being plotted. KPlotWidget automatically converts
everything to screen pixel units.

KPlotWidget draws X and Y axes with tick marks and tick labels. It
automatically determines how many tick marks to use and where they
should be, based on the data limits specified for the plot. You change
the limits by calling `setLimits(double x1, double x2, double y1,
double y2)`.

Data to be plotted are stored using the KPlotObject class. KPlotObject
consists of a QList of QPointF's, each specifying the X,Y coordinates
of a data point. KPlotObject also specifies the "type" of data to be
plotted (POINTS or CURVE or POLYGON or LABEL).

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6Plotting.so.6
%attr(755,root,root) %{_libdir}/libKF6Plotting.so.*.**
%attr(755,root,root) %{qt6dir}/plugins/designer/kplotting6widgets.so

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KPlotting
%{_libdir}/cmake/KF6Plotting
%{_libdir}/libKF6Plotting.so
