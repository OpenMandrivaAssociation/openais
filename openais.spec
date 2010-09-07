%define alphatag svn1579
%define libmajor 2
%define libname %mklibname openais %libmajor
%define develname %mklibname -d openais
%define staticname %mklibname -d -s openais

Name: openais
Summary: The openais Standards-Based Cluster Framework executive and APIs
Version: 1.1.4
Release: %mkrel 1
License: BSD
Group: System/Base
URL: http://www.openais.org/
Source0: ftp://ftp:download@ftp.openais.org/downloads/openais-%{version}/openais-%{version}.tar.gz
Requires(pre): rpm-helper
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires: corosync >= 1.1.0
Requires: %{libname} >= %{version}-%{release}
BuildRequires: corosync-devel >= 1.1.0
Patch0: openais-defaultconfig.patch
Patch1: openais-0.80.3-fix-arch-detection.patch
Patch2: openais-0.80.3-build-on-glibc2.8.patch
Patch3: openais-lsbinit.patch

BuildRoot: %{_tmppath}/%{name}-root

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
Summary: The openais Standards-Based Cluster Framework development libraries
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %develname
This package contains the libraries and include files used to develop using
openais APIs.

%package -n %staticname
Summary: The openais Standards-Based Cluster Framework static libraries
Group: Development/C
Requires: %{name}-devel = %{version}-%{release}
Provides: %{name}-static-devel = %{version}-%{release}

%description -n %staticname
This package contains the development library archives required to compile
static binaries using the openais APIs.

%prep
%setup -q -n openais-%{version}
%patch0 -p1
#patch3 -p1

%build
%configure \
	--with-lcrso-dir=$(pkg-config corosync --variable lcrsodir)

# -O3 required for performance reasons
# So we get proper debug output, for now we don't compile with O3
#CFLAGS="$(echo '%{optflags}' | sed -e 's/-O[0-9]*//') -O3"
#make CFLAGS="$CFLAGS"
#CFLAGS="$CFLAGS -D_GNU_SOURCE -D__USE_GNU"
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std STATICLIBS=NO LCRSODIR=%{_libexecdir}/lcrso
mkdir -p %{buildroot}/%{_sysconfdir}/rc.d
#install -m 755 init/generic $RPM_BUILD_ROOT%{_initrddir}/openais
mv %{buildroot}/%{_sysconfdir}/init.d %{buildroot}/%{_initrddir}
#install -m 755 test/openais-cfgtool $RPM_BUILD_ROOT%{_sbindir}
# fix install permissions and make rpmlint happy
#chmod 0755 $RPM_BUILD_ROOT%{_sbindir}/ais-keygen
mv %{buildroot}/etc/corosync/amf.conf.example %{buildroot}/etc/corosync/amf.conf

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
%doc LICENSE
%doc README.amf
%{_sbindir}/aisexec
%{_sbindir}/openais-instantiate
%config(noreplace) /etc/corosync/amf.conf
%{_initrddir}/openais
%{_libexecdir}/lcrso
%{_mandir}/man8/*.8*
%{_mandir}/man5/*.5*

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/*.so.*

%files -n %develname
%defattr(-,root,root,-)
%{_includedir}/openais/
%{_libdir}/*.so
%{_libexecdir}/pkgconfig/*.pc

%files -n %staticname
%defattr(-,root,root,-)
%{_libdir}/*.a
