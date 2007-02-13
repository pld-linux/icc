# TODO: 
# - check all licenses - maybe we can distribute it?
# - fix "szambo" in %{_bindir}, maybe move unnecesary files to %{_libdir}/icc ?
# - ia64 version ;)
%define		fileversion	9.0.021
%define		iccversion	9.0
%define		idbversion	9.0
Summary:	Intel C Compiler
Summary(pl.UTF-8):	Kompilator C Intela
Name:		icc
Version:	%{fileversion}
Release:	0.1
License:	commercial, needed license from Intel, not distributable
Group:		Development/Tools
Source0:	ftp://download.intel.com/software/products/compilers/downloads/l_cc_p_%{version}.tar.gz
# NoSource0-md5:	df3deb1b1cfe56cf64d1c7cd2e694805
NoSource:	0
URL:		http://www.intel.com
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{fileversion}-%{release}
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Intel C Compiler.

%description -l pl.UTF-8
Kompilator C Intela.

%package libs
Summary:	Libraries for programs compiled by Intel C Compiler
Summary(pl.UTF-8):	Biblioteki dla programów kompilowanych kompilatorem C Intela
Group:		Libraries

%description libs
Libraries used by programs compiled with Intel C Compiler.

%description libs -l pl.UTF-8
Biblioteki używane przez programy kompilowane za pomocą intelowskiego
kompilatora C.

%package -n idb
Summary:	Intel Debugger
Summary(pl.UTF-8):	Intelowski Debugger
Version:	%{idbversion}
Group:		Development/Debuggers

%description -n idb
Debugger for programs compiled by Intel C Compiler from Intel.

%description -n idb -l pl.UTF-8
Debugger dla programów kompilowanych kompilatorem C Intela od Intela.

%prep
%setup -q -n l_cc_p_%{fileversion}

for i in intel-*-*.i386.rpm; do
	rpm2cpio $i | cpio -i --no-absolute-filenames -d
done
sed -i -e 's|<INSTALLDIR>|%{_prefix}|g' opt/intel/cc/%{iccversion}/bin/{icc,icpc,iccvars.csh,iccvars.sh}
sed -i -e 's|<INSTALLDIR>|%{_prefix}|g' opt/intel/idb/%{idbversion}/bin/*.*sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_mandir}/man1,%{_includedir}/icc,%{_datadir}/icc/licenses}

# intel compiler
cd opt/opt/intel/cc/%{iccversion}
install bin/* $RPM_BUILD_ROOT%{_bindir}
install man/man1/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
install lib/* $RPM_BUILD_ROOT%{_libdir}
cp -r include/* $RPM_BUILD_ROOT%{_includedir}/icc
install licenses/* $RPM_BUILD_ROOT%{_datadir}/icc/licenses
cd ../..
# intel debugger
cd opt/opt/intel/idb/%{idbversion}
install bin/?idb $RPM_BUILD_ROOT%{_bindir}/idb
install man/man1/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

cat > $RPM_BUILD_ROOT%{_bindir}/icc <<'EOF'
#!/bin/sh
export INTEL_LICENSE_FILE=/usr/share/icc/licenses
exec /usr/bin/iccbin ${1:+"$@"}
EOF

cat > $RPM_BUILD_ROOT%{_bindir}/icpc <<'EOF'
#!/bin/sh
export INTEL_LICENSE_FILE=/usr/share/icc/licenses
exec /usr/bin/icpcbin ${1:+"$@"}
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc opt/intel_cc_*/doc/*
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.o
%{_includedir}/*
%{_datadir}/%{name}
%{_mandir}/man1/ic*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so.*

%files -n idb
%defattr(644,root,root,755)
%doc opt/intel_idb_*/doc/*
%attr(755,root,root) %{_bindir}/idb
%{_mandir}/man1/idb*
