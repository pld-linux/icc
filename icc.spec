# TODO: 
# - separate debugger, libraries to separated package
# - check all licenses - maybe we can distribute it?
# - fix "szambo" in %{_bindir}, maybe move unnecesary files to %{_libdir}/icc ?
# - ia64 version ;)
Summary:	Intel C Compiler
Summary(pl):	Kompilator C Intela
Name:		icc
Version:	8.0.055
Release:	0.1
License:	commercial, to run needed license from intel.
Group:		Development/Tools
Source0:	ftp://download.intel.com/software/products/compilers/downloads/l_cc_p_%{version}.tar.gz
# Source0-md5:	df3deb1b1cfe56cf64d1c7cd2e694805
URL:		http://www.intel.com
ExclusiveArch:	%{ix86}
NoSource:	0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Intel C Compilator.

%description -l pl
Kompilator C Intela.

%prep
%setup -q -n l_cc_p_%{version}

%build
rpm2cpio intel-*-*.i386.rpm |cpio -i --no-absolute-filenames -d
perl -p -i -e "s|<INSTALLDIR>|%{_prefix}|g" opt/intel_cc_80/bin/{icc,icpc,iccvars.csh,iccvars.sh}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir},%{_mandir}/man1,%{_includedir}/icc,%{_datadir}/icc/licenses}
cd opt/intel_cc_80
install bin/* $RPM_BUILD_ROOT%{_bindir}
install man/man1/*.1 $RPM_BUILD_ROOT%{_mandir}/man1
install lib/* $RPM_BUILD_ROOT%{_libdir}
cp -r include/* $RPM_BUILD_ROOT%{_includedir}/icc
install licenses/* $RPM_BUILD_ROOT%{_datadir}/icc/licenses

cat >$RPM_BUILD_ROOT%{_bindir}/icc <<EOF
#!/bin/sh
INTEL_LICENSE_FILE=/usr/share/icc/licenses;
export INTEL_LICENSE_FILE
if [ \$# != 0 ]
then
 exec /usr/bin/iccbin "\$@";
else
 exec /usr/bin/iccbin;
fi
EOF

cat >$RPM_BUILD_ROOT%{_bindir}/icpc <<EOF
#!/bin/sh
INTEL_LICENSE_FILE=/usr/share/icc/licenses;
export INTEL_LICENSE_FILE
if [ \$# != 0 ]
then
 exec /usr/bin/icpcbin "\$@";
else
 exec /usr/bin/icpcbin;
fi
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
%{_libdir}/*
%{_mandir}/man1/*
%{_includedir}/*
%{_datadir}/%{name}
%doc opt/intel_cc_80/doc/*
