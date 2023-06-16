Name:           check
Version:        0.15.2
Release:        1
Summary:        A unit testing framework for C
Source0:        https://github.com/libcheck/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
License:        LGPLv2+
URL:            http://libcheck.github.io/check/
Patch0:         %{name}-0.11.0-info-in-builddir.patch
Patch1:         %{name}-0.11.0-fp.patch

BuildRequires:  gcc libtool patchutils pkgconfig
BuildRequires:  subunit-devel texinfo

%description
Check is a unit testing framework for C. It features a simple interface for
defining unit tests, putting little in the way of the developer. Tests are
run in a separate address space, so both assertion failures and code errors
that cause segmentation faults or other signals can be caught. Test results
are reportable in the following: Subunit, TAP, XML, and a generic logging
format.

%package devel
Summary:        Libraries and headers for developing programs with check
Requires:       pkgconfig
Requires:       %{name}%{?_isa} = %{version}-%{release}

Provides:       %{name}-static
Obsoletes:      %{name}-static
Provides:       %{name}-checkmk
Obsoletes:      %{name}-checkmk

%description devel
Libraries and headers for developing programs with check.Also include checkmk
which binary translates concise versions of test suites into C programs.

%package_help


%prep
%autosetup -p1

sed -e 's/\(Check: (check)\)Introduction./\1.               A unit testing framework for C./' \
    -i doc/%{name}.texi

sed -e '/DECLS(\[a/s|)|,,,[AC_INCLUDES_DEFAULT\n[#include <time.h>\n #include <sys/time.h>]]&|' \
    -i configure.ac

find . -name .cvsignore -exec rm {} +


%build
autoreconf -fiv
%configure --disable-timeout-tests
%disable_rpath
%make_build

%install
%make_install
%delete_la
rm -rf %{buildroot}%{_infodir}/dir
rm -rf %{buildroot}%{_docdir}/%{name}


%check
export LD_LIBRARY_PATH=$PWD/src/.libs
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING.LESSER
%{_libdir}/libcheck.so.*

%files devel
%license COPYING.LESSER
%{_includedir}/*.h
%{_libdir}/libcheck.so
%{_libdir}/pkgconfig/check.pc
%{_datadir}/aclocal/check.m4
%{_libdir}/libcheck.a
%{_bindir}/checkmk
%doc doc/example
%doc checkmk/examples checkmk/test
%exclude %{_docdir}/checkmk/test/check_checkmk*
%exclude %{_docdir}/checkmk/test/empty_input

%files help
%doc AUTHORS ChangeLog
%doc checkmk/README
%{_infodir}/check*
%{_mandir}/man1/checkmk.1*

%changelog
* Wed Jan 19 2022 SimpleUpdate Robot <tc@openeuler.org> - 0.15.2-1
- Upgrade to version 0.15.2

* Mon Dec 9 2019 mengxian <mengxian@huawei.com> - 0.12.0-4
- Package init
