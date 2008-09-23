%define alphatag svn1579
%define libmajor 2
%define libname %mklibname openais %libmajor
%define develname %mklibname -d openais

Name: openais
Summary: The openais Standards-Based Cluster Framework executive and APIs
Version: 0.80.3
Release: %mkrel 3
License: BSD
Group: System/Base
URL: http://developer.osdl.org/dev/openais/
Source0: http://developer.osdl.org/dev/openais/downloads/openais-%{version}/openais-%{version}.tar.gz
Requires(pre): rpm-helper
Requires(post): rpm-helper
Requires(preun): rpm-helper
Patch0: openais-defaultconfig.patch
Patch1: openais-0.80.3-fix-arch-detection.patch
Patch2: openais-0.80.3-build-on-glibc2.8.patch

BuildRoot: %{_tmppath}/%{name}-root

%define ais_user_uid 39

%description 
This package contains the openais executive, openais service handlers,
default configuration files and init script.

%package -n %libname
Summary: The openais Standards-Based Cluster Framework libraries
Group: System/Libraries

%description -n %libname
This package contains the shared libraries and include files implementing 
openais APIs.

%package -n %develname
Summary: The openais Standards-Based Cluster Framework libraries
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %develname
This package contains the libraries and include files used to develop using
openais APIs.

%prep
%setup -q -n openais-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
perl -pi -e 's,/usr/libexec/lcrso,%{_libexecdir}/lcrso,g'  lcr/lcr_ifact.c

%build

# -O3 required for performance reasons
# So we get proper debug output, for now we don't compile with O3
#CFLAGS="$(echo '%{optflags}' | sed -e 's/-O[0-9]*//') -O3"
#make CFLAGS="$CFLAGS"
CFLAGS="$CFLAGS -D_GNU_SOURCE -D__USE_GNU"
make LCRSODIR=%{_libexecdir}/lcrso

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std STATICLIBS=NO LCRSODIR=%{_libexecdir}/lcrso
mkdir -p $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_initrddir}
install -m 644 LICENSE SECURITY README.devmap README.amf \
 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/
install -m 755 init/redhat $RPM_BUILD_ROOT%{_initrddir}/openais
install -m 755 test/openais-cfgtool $RPM_BUILD_ROOT%{_sbindir}
# fix install permissions and make rpmlint happy
chmod 0755 $RPM_BUILD_ROOT%{_sbindir}/ais-keygen

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%_pre_useradd ais / /sbin/nologin

%post
%_post_service openais
/sbin/ldconfig > /dev/null

%preun
%_preun_service openais

%postun
%_postun_userdel ais

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%postun -n %libname -p /sbin/ldconfig
%endif

%files 
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/LICENSE
%doc %{_docdir}/%{name}-%{version}/SECURITY
%doc %{_docdir}/%{name}-%{version}/README.amf
%{_sbindir}/aisexec
%{_sbindir}/ais-keygen
%{_sbindir}/openais-cfgtool
%dir /etc/ais
%config(noreplace) /etc/ais/openais.conf
%config(noreplace) /etc/ais/amf.conf
%config(noreplace) /etc/ld.so.conf.d/openais-*.conf
%{_initrddir}/openais
%{_libexecdir}/lcrso
%{_mandir}/man8/*.8*
%{_mandir}/man5/*.5*

%files -n %libname
%defattr(-,root,root,-)
%dir %{_libdir}/openais
%{_libdir}/openais/*.so.*

%files -n %develname
%defattr(-,root,root,-)
%dir %{_docdir}/%{name}-%{version}
%doc %{_docdir}/%{name}-%{version}/README.devmap
%{_includedir}/openais/
%{_libdir}/openais/*.so*
%{_mandir}/man3/*.3.*

