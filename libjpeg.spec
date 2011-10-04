Summary: A library for manipulating JPEG image format files
Name: libjpeg
Version: 6b
Release: 43
License: IJG
Group: System/Libraries
URL: http://www.ijg.org/

Source0: http://downloads.sourceforge.net/project/libjpeg/libjpeg/6b/jpegsrc.v6b.tar.gz
Source1: configure.in

Patch1: jpeg-c++.patch
Patch4: libjpeg-cflags.patch
Patch5: libjpeg-buf-oflo.patch
Patch6: libjpeg-autoconf.patch
Patch7: libjpeg-arm-arch.patch

BuildRequires: autoconf libtool
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
Requires: libjpeg = %{version}-%{release}

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
Requires: libjpeg-devel = %{version}-%{release}

%description static
The libjpeg-static package contains the statically linkable version of libjpeg.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%prep
%setup -q -n jpeg-6b

%patch1 -p1 -b .c++
%patch4 -p1 -b .cflags
%patch5 -p1 -b .oflo
%patch6 -p1
%patch7 -p1

# For long-obsolete reasons, libjpeg 6b doesn't ship with a configure.in.
# We need to re-autoconf though, in order to update libtool support,
# so supply configure.in.
cp %{SOURCE1} configure.in

# libjpeg 6b includes a horribly obsolete version of libtool.
# Blow it away and replace with build system's version.
rm -f config.guess ltmain.sh ltconfig aclocal.m4
aclocal
libtoolize
autoconf

%build
%configure --enable-shared --enable-static

make libdir=%{_libdir} %{?_smp_mflags}

LD_LIBRARY_PATH=$PWD:$LD_LIBRARY_PATH make test

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/usr/{include,bin}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

%makeinstall

# Work around the broken makefiles...
mv $RPM_BUILD_ROOT%{_mandir}/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# We don't ship .la files.
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc usage.doc README
%{_libdir}/libjpeg.so.*
%{_bindir}/*
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%doc libjpeg.doc coderules.doc structure.doc wizard.doc example.c
%{_libdir}/*.so
/usr/include/*.h

%files static
%defattr(-,root,root)
%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

