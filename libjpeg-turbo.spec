Summary: A library for manipulating JPEG image format files
Name: libjpeg-turbo
Version: 1.2.0
Release: 0
License: IJG
Group: System/Libraries
URL: http://www.libjpeg-turbo.org/

Source0: libjpeg-turbo-%{version}.tar.gz

BuildRequires: autoconf libtool nasm
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The libjpeg package contains a library of functions for manipulating
JPEG images, as well as simple client programs for accessing the
libjpeg functions.  Libjpeg client programs include cjpeg, djpeg,
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into
JPEG format.  Djpeg decompresses a JPEG file into a regular image
file.  Jpegtran can perform various useful transformations on JPEG
files.  Rdjpgcom displays any text comments included in a JPEG file.
Wrjpgcom inserts text comments into a JPEG file.

%package devel
Summary: Development tools for programs which will use the libjpeg library
Group: Development/Libraries
Requires: libjpeg-turbo = %{version}-%{release}
Provides: libjpeg-devel

%description devel
The libjpeg-devel package includes the header files and documentation
necessary for developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

%package static
Summary: Static JPEG image format file library
Group: Development/Libraries
Requires: libjpeg-turbo-devel = %{version}-%{release}
Provides: libjpeg-static

%description static
The libjpeg-static package contains the statically linkable version of libjpeg.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%prep
%setup -q -n libjpeg-turbo-%{version}

%build
%configure --enable-shared --enable-static

make libdir=%{_libdir} %{?_smp_mflags}

LD_LIBRARY_PATH=$PWD:$LD_LIBRARY_PATH make test

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall

# We don't ship .la files.
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT/usr/share/doc

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc README
%{_libdir}/libjpeg.so.*
%{_bindir}/*
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
/usr/include/*.h

%files static
%defattr(-,root,root)
%{_libdir}/*.a
