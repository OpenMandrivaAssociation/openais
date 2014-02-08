%define alphatag svn1579
%define major	3
%define maj4	4
%define	libSaAmf	%mklibname libSaAmf %{major}
%define	libSaCkpt	%mklibname libSaCkpt %{major}
%define	libSaLck	%mklibname libSaLck %{major}
%define	libSaEvt	%mklibname libSaEvt %{major}
%define	libSaClm	%mklibname libSaClm %{major}
%define	libSaTmr	%mklibname libSaTmr %{major}
%define	libSaMsg	%mklibname libSaMsg %{maj4}
%define devname	%mklibname -d %{name}

Summary:	The openais Standards-Based Cluster Framework executive and APIs
Name:		openais
Version:	1.1.4
Release:	6
License:	BSD
Group:		System/Base
Url:		http://www.openais.org/
Source0:	ftp://ftp:download@ftp.openais.org/downloads/%{name}-%{version}/openais-%{version}.tar.gz
Patch0:		openais-defaultconfig.patch

BuildRequires:	pkgconfig(libcoroipcc)
Requires(pre,post,preun):	rpm-helper
Requires:	corosync >= 1.1.0

%description 
This package contains the openais executive, openais service handlers,
default configuration files and init script.

%package -n %{libSaAmf}
Summary:	The openais Standards-Based Cluster Framework libraries
Group:		System/Libraries
Obsoletes:	%{_lib}openais2 < 1.1.4-5

%description -n %{libSaAmf}
This package contains the shared libraries and include files implementing 
openais APIs.

%package -n %{libSaCkpt}
Summary:	The openais Standards-Based Cluster Framework libraries
Group:		System/Libraries
Conflicts:	%{_lib}openais2 < 1.1.4-5

%description -n %{libSaCkpt}
This package contains the shared libraries and include files implementing 
openais APIs.

%package -n %{libSaLck}
Summary:	The openais Standards-Based Cluster Framework libraries
Group:		System/Libraries
Conflicts:	%{_lib}openais2 < 1.1.4-5

%description -n %{libSaLck}
This package contains the shared libraries and include files implementing 
openais APIs.

%package -n %{libSaEvt}
Summary:	The openais Standards-Based Cluster Framework libraries
Group:		System/Libraries
Conflicts:	%{_lib}openais2 < 1.1.4-5

%description -n %{libSaEvt}
This package contains the shared libraries and include files implementing 
openais APIs.

%package -n %{libSaClm}
Summary:	The openais Standards-Based Cluster Framework libraries
Group:		System/Libraries
Conflicts:	%{_lib}openais2 < 1.1.4-5

%description -n %{libSaClm}
This package contains the shared libraries and include files implementing 
openais APIs.

%package -n %{libSaTmr}
Summary:	The openais Standards-Based Cluster Framework libraries
Group:		System/Libraries
Conflicts:	%{_lib}openais2 < 1.1.4-5

%description -n %{libSaTmr}
This package contains the shared libraries and include files implementing 
openais APIs.

%package -n %{libSaMsg}
Summary:	The openais Standards-Based Cluster Framework libraries
Group:		System/Libraries
Conflicts:	%{_lib}openais2 < 1.1.4-5

%description -n %{libSaMsg}
This package contains the shared libraries and include files implementing 
openais APIs.

%package -n %{devname}
Summary:	The openais Standards-Based Cluster Framework development libraries
Group:		Development/C
Requires:	%{libSaAmf} = %{version}-%{release}
Requires:	%{libSaCkpt} = %{version}-%{release}
Requires:	%{libSaLck} = %{version}-%{release}
Requires:	%{libSaEvt} = %{version}-%{release}
Requires:	%{libSaClm} = %{version}-%{release}
Requires:	%{libSaTmr} = %{version}-%{release}
Requires:	%{libSaMsg} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Obsoletes:	%{_lib}openais-static-devel = %{version}-%{release}

%description -n %{devname}
This package contains the libraries and include files used to develop using
openais APIs.

%prep
%setup -q
%apply_patches

%build
%configure2_5x \
	--disable-static \
	--with-lcrso-dir=$(pkg-config corosync --variable lcrsodir)

# -O3 required for performance reasons
# So we get proper debug output, for now we don't compile with O3
#CFLAGS="$(echo '%{optflags}' | sed -e 's/-O[0-9]*//') -O3"
#make CFLAGS="$CFLAGS"
#CFLAGS="$CFLAGS -D_GNU_SOURCE -D__USE_GNU"
%make

%install
%makeinstall_std STATICLIBS=NO LCRSODIR=%{_libexecdir}/lcrso
mkdir -p %{buildroot}/%{_sysconfdir}/rc.d
mv %{buildroot}/%{_sysconfdir}/init.d %{buildroot}/%{_initrddir}
#install -m 755 test/openais-cfgtool %{buildroot}%{_sbindir}
# fix install permissions and make rpmlint happy
#chmod 0755 %{buildroot}%{_sbindir}/ais-keygen
mv %{buildroot}/etc/corosync/amf.conf.example %{buildroot}/etc/corosync/amf.conf

rm -f %{buildroot}%{_libdir}/*.a

%pre
%_pre_useradd ais / /sbin/nologin

%post
%_post_service %{name}
/sbin/ldconfig > /dev/null

%preun
%_preun_service %{name}

%postun
%_postun_userdel ais

%files 
%doc LICENSE
%doc README.amf
%config(noreplace) /etc/corosync/amf.conf
%{_sbindir}/aisexec
%{_sbindir}/openais-instantiate
%{_initrddir}/openais
%{_libexecdir}/lcrso
%{_mandir}/man8/*.8*
%{_mandir}/man5/*.5*

%files -n %{libSaAmf}
%{_libdir}/libSaAmf.so.%{major}*

%files -n %{libSaCkpt}
%{_libdir}/libSaCkpt.so.%{major}*

%files -n %{libSaLck}
%{_libdir}/libSaLck.so.%{major}*

%files -n %{libSaEvt}
%{_libdir}/libSaEvt.so.%{major}*

%files -n %{libSaClm}
%{_libdir}/libSaClm.so.%{major}*

%files -n %{libSaTmr}
%{_libdir}/libSaTmr.so.%{major}*

%files -n %{libSaMsg}
%{_libdir}/libSaMsg.so.%{maj4}*

%files -n %{devname}
%{_includedir}/openais/
%{_libdir}/*.so
%{_libexecdir}/pkgconfig/*.pc

