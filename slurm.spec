# Obsolete EVR
%global obs_evr 17.02.9-4

# Upstream tarballs use an additional release number
%global ups_rel 2

%if "%{ups_rel}" == "1"
%global name_version %{name}-%{version}
%else
%global name_version %{name}-%{version}-%{ups_rel}
%endif

# Allow linkage with undefined symbols (disable -z,defs)
%undefine _strict_symbol_defs_build

# Allow dlopen with unresolved symbols (disable -z,now)
%define _hardened_ldflags "-Wl,-z,lazy"

Name:           slurm
Version:        17.11.3
Release:        1%{?dist}
Summary:        Simple Linux Utility for Resource Management
License:        GPLv2 and BSD
URL:            https://slurm.schedmd.com/
Source0:        http://www.schedmd.com/download/latest/%{name_version}.tar.bz2
Source1:        slurm.conf
Source2:        slurmdbd.conf
Source3:        slurm-sview.desktop
Source4:        slurm-128x128.png
Source5:        slurm-setuser.in

# Upstream bug #4449: release-style versioning of libslurmfull
Patch0:         slurm_libslurmfull_version.patch

# Build-related patches
Patch10:        slurm_perlapi_rpaths.patch
Patch11:        slurm_html_doc_path.patch
Patch12:        slurm_doc_fix.patch

# Fedora-related patches
Patch20:        slurm_pmix_soname.patch
Patch21:        slurm_service_files.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  environment(modules)
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-podlators
BuildRequires:  pkgconf
BuildRequires:  pkgconfig(check)
%{?systemd_requires}
BuildRequires:  systemd

BuildRequires:  hdf5-devel
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(hwloc)
BuildRequires:  pkgconfig(libfreeipmi)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(librrd)
BuildRequires:  pkgconfig(libssh2)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(mariadb)
BuildRequires:  pkgconfig(munge)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(pmix) >= 2.0.0
BuildRequires:  pkgconfig(zlib)
BuildRequires:  readline-devel

# follow arch exclusions for these devel packages
%ifnarch s390 s390x %{arm}
BuildRequires:  libibmad-devel
BuildRequires:  libibumad-devel
BuildRequires:  numactl-devel
%endif

Requires:       munge
Requires:       pmix >= 2.0.0

Obsoletes:      %{name} <= %{obs_evr}
Obsoletes:      %{name}-plugins <= %{obs_evr}
Obsoletes:      %{name}-plugins-auth_none <= %{obs_evr}
Obsoletes:      %{name}-plugins-lua <= %{obs_evr}
Obsoletes:      %{name}-plugins-munge <= %{obs_evr}
Obsoletes:      %{name}-plugins-mysql <= %{obs_evr}

%description
Slurm is an open source, fault-tolerant, and highly scalable
cluster management and job scheduling system for large and
small Linux clusters.

# -------------
# Base Packages
# -------------

%package devel
Summary: Slurm development
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description devel
Development package for Slurm.  Includes headers, libraries
and man pages for using the Slurm API.

%package doc
Summary: Slurm documentation
%description doc
Documentation package for Slurm.  Includes documentation and
html-based configuration tools for Slurm.

%package gui
Summary: Slurm gui and visual tools
Requires: %{name}%{?_isa} = %{version}-%{release}
%description gui
This package contains the Slurm visual tools smap and sview
and their respective man pages.

%package libs
Summary: Slurm shared libraries
Provides: pmi
Requires: environment(modules)
%description libs
Slurm shared libraries.

%package rrdtool
Summary: Slurm rrdtool external sensor plugin
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-plugins-rrdtool <= %{obs_evr}
%description rrdtool
Slurm external sensor plugin for rrdtool. This package is separated from
the base plugins package due to gui dependencies which are unneeded if not
using this plugin.

%package slurmctld
Summary: Slurm controller daemon
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: %{name} <= %{obs_evr}
%description slurmctld
Slurm controller daemon. Used to manage the job queue, schedule jobs,
and dispatch RPC messages to the slurmd processon the compute nodes
to launch jobs.

%package slurmd
Summary: Slurm compute node daemon
Requires: %{name}%{?_isa} = %{version}-%{release}
Obsoletes: %{name} <= %{obs_evr}
%description slurmd
Slurm compute node daemon. Used to launch jobs on compute nodes

%package slurmdbd
Summary: Slurm database daemon
Requires: %{name}%{?_isa} = %{version}-%{release}
%description slurmdbd
Slurm database daemon. Used to accept and process database RPCs and upload
database changes to slurmctld daemons on each cluster.

# -----------------
# Contribs Packages
# -----------------

%package contribs
Summary: Perl tools to print Slurm job state information
Requires: %{name}-perlapi%{?_isa} = %{version}-%{release}
%description contribs
Slurm contribution package which includes the programs seff,
sjobexitmod, sjstat and smail.  See their respective man pages
for more information.

%package openlava
Summary: Openlava/LSF wrappers for transition from OpenLava/LSF to Slurm
Requires: %{name}-perlapi%{?_isa} = %{version}-%{release}
%description openlava
OpenLava wrapper scripts used for helping migrate from OpenLava/LSF to Slurm.

%package perlapi
Summary: Perl API to Slurm
Requires: perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description perlapi
Perl API package for Slurm.  This package includes the perl API to provide a
helpful interface to Slurm through Perl.

%package pam_slurm
Summary: Slurm pam modules
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-plugins-pam_slurm <= %{obs_evr}
%description pam_slurm
The pam_slurm module restricts access to compute nodes in a cluster where Slurm
is in use.  Also includes the pam_slurm_adopt plugin for "adopting" connections
into slurm jobs.

%package torque
Summary: Torque/PBS wrappers for transition from Torque/PBS to Slurm
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-perlapi%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-plugins-pbs <= %{obs_evr}
%description torque
Torque wrapper scripts used for helping migrate from Torque/PBS to Slurm.

%prep
%setup -q -n %{name_version}
%patch0 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch20 -p1
%patch21 -p1
cp %SOURCE1 etc/slurm.conf
cp %SOURCE1 etc/slurm.conf.example
cp %SOURCE2 etc/slurmdbd.conf
cp %SOURCE2 etc/slurmdbd.conf.example
mkdir -p share/applications
mkdir -p share/icons/hicolor/128x128/apps
cp %SOURCE3 share/applications/%{name}-sview.desktop
cp %SOURCE4 share/icons/hicolor/128x128/apps/%{name}.png
mkdir -p extras
cp %SOURCE5 extras/%{name}-setuser.in

%build
%{__aclocal} -I auxdir
%{__autoconf}
%{__automake} --no-force
%configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir}/%{name} \
  --with-pam_dir=%{_libdir}/security \
  --with-pmix \
  --enable-shared \
  --enable-x11 \
  --disable-static \
  --disable-debug \
  --disable-developer \
  --disable-salloc-background \
  --disable-multiple-slurmd \
  --disable-partial_attach \
  --with-shared-libslurm \
  --without-rpath
# patch libtool to remove rpaths
sed -i 's|^hardcode_into_libs=.*|hardcode_into_libs=no|g' libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

# configure extras/slurm-setuser script
sed -r '
s|^dir_conf=.*|dir_conf="%{_sysconfdir}/%{name}"|g;
s|^dir_log=.*|dir_log="%{_var}/log/%{name}"|g;
s|^dir_run=.*|dir_run="%{_rundir}/%{name}"|g;
s|^dir_spool=.*|dir_spool="%{_var}/spool/%{name}"|g;
s|^dir_tmpfiles_d=.*|dir_tmpfiles_d="%{_tmpfilesdir}"|g;' \
    extras/%{name}-setuser.in > extras/%{name}-setuser

# build base packages
%make_build V=1

# build contribs packages
# INSTALLDIRS=vendor so perlapi goes to vendor_perl directory
PERL_MM_PARAMS="INSTALLDIRS=vendor" %make_build contrib V=1

%check
# The test binaries need LD_LIBRARY_PATH to find the compiled slurm library
# in the build tree.
LD_LIBRARY_PATH="%{buildroot}%{_libdir};%{_libdir}" %{__make} check

%install
%make_install
%{__make} install-contrib DESTDIR=%{buildroot}

install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}
install -d -m 0755 %{buildroot}%{_sysconfdir}/%{name}/layouts.d
install -d -m 0755 %{buildroot}%{_unitdir}
install -m 0644 -p etc/cgroup.conf.example \
    %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -p etc/cgroup.conf.example \
    %{buildroot}%{_sysconfdir}/%{name}/cgroup.conf
install -m 0644 -p etc/cgroup_allowed_devices_file.conf.example \
    %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -p etc/layouts.d.power.conf.example \
    %{buildroot}%{_sysconfdir}/%{name}/layouts.d/power.conf.example
install -m 0644 -p etc/layouts.d.power_cpufreq.conf.example \
    %{buildroot}%{_sysconfdir}/%{name}/layouts.d/power_cpufreq.conf.example
install -m 0644 -p etc/layouts.d.unit.conf.example \
    %{buildroot}%{_sysconfdir}/%{name}/layouts.d/unit.conf.example
install -m 0644 -p etc/slurm.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -p etc/slurm.conf.example %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -p etc/slurmdbd.conf %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -p etc/slurmdbd.conf.example %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -p etc/slurm.epilog.clean %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 -p etc/slurmctld.service %{buildroot}%{_unitdir}
install -m 0644 -p etc/slurmd.service %{buildroot}%{_unitdir}
install -m 0644 -p etc/slurmdbd.service %{buildroot}%{_unitdir}

# tmpfiles.d file for creating /run/slurm dir after reboot
install -d -m 0755 %{buildroot}%{_tmpfilesdir}
cat  >%{buildroot}%{_tmpfilesdir}/%{name}.conf <<EOF
D %{_rundir}/%{name} 0755 root root -
EOF

# logrotate.d file for /var/log/slurm logging
install -d -m 0755 %{buildroot}%{_var}/log/%{name}
install -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
cat >%{buildroot}%{_sysconfdir}/logrotate.d/%{name} <<EOF
%{_var}/log/%{name}/* {
    missingok
    notifempty
    copytruncate
    rotate 5
}
EOF

# /var/run/slurm, /var/spool/slurm dirs, (ghost) pid files
install -d -m 0755 %{buildroot}%{_rundir}/%{name}
install -d -m 0755 %{buildroot}%{_var}/spool/%{name}/ctld
install -d -m 0755 %{buildroot}%{_var}/spool/%{name}/d
touch %{buildroot}%{_rundir}/%{name}/slurmctld.pid
touch %{buildroot}%{_rundir}/%{name}/slurmd.pid
touch %{buildroot}%{_rundir}/%{name}/slurmdbd.pid

# install pmi/slurm environment module file
install -d -m 0755 %{buildroot}%{_modulesdir}/pmi
cat >%{buildroot}%{_modulesdir}/pmi/%{name}-%{_arch} <<EOF
#%%Module 1.0
#
#  pmi/slurm module for use with 'environment-modules' package:
#
conflict         pmi
prepend-path     LD_LIBRARY_PATH    %{_libdir}/%{name}/lib
prepend-path     PKG_CONFIG_PATH    %{_libdir}/%{name}/lib/pkgconfig
EOF

# install pkgconfig file slurm.pc
install -d -m 0755 %{buildroot}%{_libdir}/pkgconfig
cat >%{buildroot}%{_libdir}/pkgconfig/%{name}.pc <<EOF
includedir=%{_includedir}/%{name}
libdir=%{_libdir}

Name: %{name}
Version: %{version}
Description: Slurm development library
Cflags: -I\${includedir}
Libs: -L\${libdir} -lslurm
EOF

# install pkgconfig file pmi.pc for environment module usage
install -d -m 0755 %{buildroot}%{_libdir}/%{name}/lib/pkgconfig
cat >%{buildroot}%{_libdir}/%{name}/lib/pkgconfig/pmi.pc <<EOF
includedir=%{_includedir}/%{name}
libdir=%{_libdir}/%{name}/lib

Name: pmi
Version: %{version}
Description: Slurm PMI development library
Cflags: -I\${includedir}
Libs: -L\${libdir} -lpmi
EOF

# install pkgconfig file pmi2.pc for environment module usage
install -d -m 0755 %{buildroot}%{_libdir}/%{name}/lib/pkgconfig
cat >%{buildroot}%{_libdir}/%{name}/lib/pkgconfig/pmi2.pc <<EOF
includedir=%{_includedir}/%{name}
libdir=%{_libdir}/%{name}/lib

Name: pmi2
Version: %{version}
Description: Slurm PMI2 development library
Cflags: -I\${includedir}
Libs: -L\${libdir} -lpmi2
EOF

# install desktop file for sview GTK+ program
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    share/applications/%{name}-sview.desktop

# install desktop icon for sview GTK+ program
install -d -m 0755 %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -m 0644 share/icons/hicolor/128x128/apps/%{name}.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# install the extras/slurm-setuser script
install -m 0755 extras/%{name}-setuser \
    %{buildroot}%{_bindir}/%{name}-setuser

# move libpmi/libpmi2 to pmi/slurm environment module location
install -d -m 0755 %{buildroot}%{_libdir}/%{name}/lib
mv %{buildroot}%{_libdir}/libpmi.so* %{buildroot}%{_libdir}/%{name}/lib
mv %{buildroot}%{_libdir}/libpmi2.so* %{buildroot}%{_libdir}/%{name}/lib

install -m 0755 contribs/sjstat %{buildroot}%{_bindir}/sjstat

# fix perms on these files so debug info is extracted without error
chmod 0755 %{buildroot}%{perl_vendorarch}/auto/Slurm/Slurm.so
chmod 0755 %{buildroot}%{perl_vendorarch}/auto/Slurmdb/Slurmdb.so

# build man pages for contribs perl scripts
for prog in sjobexitmod sjstat mpiexec pbsnodes qalter qdel qhold qrerun qrls \
    qstat qsub bjobs bkill bsub lsid
do
    rm -f %{buildroot}%{_mandir}/man1/${prog}.1
    pod2man %{buildroot}%{_bindir}/${prog} > %{buildroot}%{_mandir}/man1/${prog}.1
done

# contribs docs
install -d -m 0755 %{buildroot}%{_docdir}/%{name}/contribs/lua
install -m 0644 contribs/README %{buildroot}%{_docdir}/%{name}/contribs
install -m 0644 contribs/lua/proctrack.lua %{buildroot}%{_docdir}/%{name}/contribs/lua

# remove libtool archives
find %{buildroot} -name \*.a -o -name \*.la | xargs rm -f
# remove libslurmfull symlink (non-development, internal library)
rm -rf %{buildroot}%{_libdir}/libslurmfull.so
# remove auth_none plugin
rm -f %{buildroot}%{_libdir}/%{name}/auth_none.so
# remove example plugins
rm -f %{buildroot}%{_libdir}/%{name}/job_submit_defaults.so
rm -f %{buildroot}%{_libdir}/%{name}/job_submit_logging.so
rm -f %{buildroot}%{_libdir}/%{name}/job_submit_partition.so
# remove bluegene files
rm -f %{buildroot}%{_libdir}/%{name}/select_bluegene.so
rm -f %{buildroot}%{_mandir}/man5/bluegene*
# remove cray files
rm -f %{buildroot}%{_libdir}/%{name}/acct_gather_energy_cray.so
rm -f %{buildroot}%{_libdir}/%{name}/core_spec_cray.so
rm -f %{buildroot}%{_libdir}/%{name}/job_container_cncu.so
rm -f %{buildroot}%{_libdir}/%{name}/job_submit_cray.so
rm -f %{buildroot}%{_libdir}/%{name}/select_alps.so
rm -f %{buildroot}%{_libdir}/%{name}/select_cray.so
rm -f %{buildroot}%{_libdir}/%{name}/switch_cray.so
rm -f %{buildroot}%{_libdir}/%{name}/task_cray.so
rm -f %{buildroot}%{_mandir}/man5/cray*
# remove perl cruft
rm -f %{buildroot}%{perl_vendorarch}/auto/Slurm*/.packlist
rm -f %{buildroot}%{perl_vendorarch}/auto/Slurm*/Slurm*.bs
rm -f %{buildroot}%{perl_archlib}/perllocal.pod

%ldconfig_scriptlets -n devel
%ldconfig_scriptlets -n lib

# -----
# Slurm
# -----

%files
%doc CONTRIBUTING.md DISCLAIMER META NEWS README.rst RELEASE_NOTES
%license COPYING LICENSE.OpenSSL
%dir %{_libdir}/%{name}
%dir %{_rundir}/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/layouts.d
%dir %{_var}/log/%{name}
%dir %{_var}/spool/%{name}
%dir %{_var}/spool/%{name}/ctld
%dir %{_var}/spool/%{name}/d
%attr(0755,root,root) %{_sysconfdir}/%{name}/slurm.epilog.clean
%config(noreplace) %{_sysconfdir}/%{name}/cgroup*.conf
%config(noreplace) %{_sysconfdir}/%{name}/slurm.conf
%{_bindir}/{sacct,sacctmgr,salloc,sattach,sbatch,sbcast}
%{_bindir}/{scancel,scontrol,sdiag,sh5util,sinfo,sprio}
%{_bindir}/{squeue,sreport,srun,sshare,sstat,strigger}
%{_bindir}/%{name}-setuser
%{_libdir}/%{name}/accounting_storage_{filetxt,none,slurmdbd}.so
%{_libdir}/%{name}/acct_gather_energy_{ibmaem,ipmi,none,rapl}.so
%{_libdir}/%{name}/acct_gather_filesystem_{lustre,none}.so
%{_libdir}/%{name}/acct_gather_interconnect_{none,ofed}.so
%{_libdir}/%{name}/acct_gather_profile_{hdf5,none}.so
%{_libdir}/%{name}/auth_munge.so
%{_libdir}/%{name}/burst_buffer_generic.so
%{_libdir}/%{name}/checkpoint_{none,ompi}.so
%{_libdir}/%{name}/core_spec_none.so
%{_libdir}/%{name}/crypto_munge.so
%{_libdir}/%{name}/crypto_openssl.so
%{_libdir}/%{name}/ext_sensors_none.so
%{_libdir}/%{name}/gres_{gpu,mic,nic}.so
%{_libdir}/%{name}/job_container_none.so
%{_libdir}/%{name}/job_submit_all_partitions.so
%{_libdir}/%{name}/job_submit_lua.so
%{_libdir}/%{name}/job_submit_require_timelimit.so
%{_libdir}/%{name}/job_submit_throttle.so
%{_libdir}/%{name}/jobacct_gather_{cgroup,linux,none}.so
%{_libdir}/%{name}/jobcomp_{elasticsearch,filetxt,mysql,none,script}.so
%{_libdir}/%{name}/launch_slurm.so
%{_libdir}/%{name}/layouts_power_{cpufreq,default}.so
%{_libdir}/%{name}/layouts_unit_default.so
%{_libdir}/%{name}/mcs_{account,group,none,user}.so
%{_libdir}/%{name}/mpi_{none,openmpi,pmi2,pmix*}.so
%{_libdir}/%{name}/node_features_knl_generic.so
%{_libdir}/%{name}/power_none.so
%{_libdir}/%{name}/preempt_{job_prio,none,partition_prio,qos}.so
%{_libdir}/%{name}/priority_{basic,multifactor}.so
%{_libdir}/%{name}/proctrack_{cgroup,linuxproc,lua,pgid}.so
%{_libdir}/%{name}/route_{default,topology}.so
%{_libdir}/%{name}/sched_{backfill,builtin,hold}.so
%{_libdir}/%{name}/select_{cons_res,linear,serial}.so
%{_libdir}/%{name}/slurmctld_nonstop.so
%{_libdir}/%{name}/switch_{generic,none}.so
%{_libdir}/%{name}/task_{affinity,cgroup,none}.so
%{_libdir}/%{name}/topology_{3d_torus,hypercube,node_rank,none,tree}.so
%{_mandir}/man1/{sacct,sacctmgr,salloc,sattach,sbatch,sbcast}.1*
%{_mandir}/man1/{scancel,scontrol,sdiag,sh5util,sinfo,sprio}.1*
%{_mandir}/man1/{squeue,sreport,srun,sshare,sstat,strigger}.1*
%{_mandir}/man1/slurm.1*
%{_mandir}/man5/acct_gather.conf.5*
%{_mandir}/man5/burst_buffer.conf.5*
%{_mandir}/man5/cgroup.conf.5*
%{_mandir}/man5/ext_sensors.conf.5*
%{_mandir}/man5/gres.conf.5*
%{_mandir}/man5/knl.conf.5*
%{_mandir}/man5/nonstop.conf.5*
%{_mandir}/man5/slurm.conf.5*
%{_mandir}/man5/topology.conf.5*
%{_mandir}/man8/spank.8*
%{_sysconfdir}/logrotate.d/%{name}
%{_sysconfdir}/%{name}/cgroup*.conf.example
%{_sysconfdir}/%{name}/layouts.d/*.example
%{_sysconfdir}/%{name}/slurm.conf.example
%{_tmpfilesdir}/slurm.conf

# -----------
# Slurm-devel
# -----------

%files devel
%dir %{_includedir}/%{name}
%dir %{_libdir}/%{name}/lib/pkgconfig
%dir %{_libdir}/%{name}/src
%dir %{_libdir}/%{name}/src/sattach
%dir %{_libdir}/%{name}/src/srun
%{_includedir}/%{name}/pmi*.h
%{_includedir}/%{name}/slurm.h
%{_includedir}/%{name}/slurm_errno.h
%{_includedir}/%{name}/slurmdb.h
%{_includedir}/%{name}/smd_ns.h
%{_includedir}/%{name}/spank.h
%{_libdir}/lib{slurm,slurmdb}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/%{name}/lib/libpmi*.so
%{_libdir}/%{name}/lib/pkgconfig/*.pc
%{_libdir}/%{name}/src/sattach/sattach.wrapper.c
%{_libdir}/%{name}/src/srun/srun.wrapper.c
%{_mandir}/man3/*.3.*

# ---------
# Slurm-doc
# ---------

%files doc
%dir %{_docdir}/%{name}
%dir %{_docdir}/%{name}/html
%{_docdir}/%{name}/html/*

# ---------
# Slurm-gui
# ---------

%files gui
%{_bindir}/smap
%{_bindir}/sview
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_mandir}/man1/smap.1*
%{_mandir}/man1/sview.1*

# ----------
# Slurm-libs
# ----------

%files libs
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/lib
%dir %{_modulesdir}/pmi
%{_libdir}/libslurm.so.*
%{_libdir}/libslurmdb.so.*
%{_libdir}/libslurmfull-*.so
%{_libdir}/%{name}/lib/libpmi*.so.*
%{_modulesdir}/pmi/*

# -------------
# Slurm-rrdtool
# -------------

%files rrdtool
%{_libdir}/%{name}/ext_sensors_rrd.so

# ---------
# Slurmctld
# ---------

%files slurmctld
%{_mandir}/man8/slurmctld.8*
%{_sbindir}/slurmctld
%{_unitdir}/slurmctld.service
%ghost %{_rundir}/%{name}/slurmctld.pid

# ------
# Slurmd
# ------

%files slurmd
%{_mandir}/man8/slurmd.8*
%{_mandir}/man8/slurmstepd.8*
%{_sbindir}/slurmd
%{_sbindir}/slurmstepd
%{_unitdir}/slurmd.service
%ghost %{_rundir}/%{name}/slurmd.pid

# --------
# Slurmdbd
# --------

%files slurmdbd
%config(noreplace) %{_sysconfdir}/%{name}/slurmdbd.conf
%{_libdir}/%{name}/accounting_storage_mysql.so
%{_mandir}/man5/slurmdbd.conf.5*
%{_mandir}/man8/slurmdbd.8*
%{_sbindir}/slurmdbd
%{_sysconfdir}/%{name}/slurmdbd.conf.example
%{_unitdir}/slurmdbd.service
%ghost %{_rundir}/%{name}/slurmdbd.pid

# --------------
# Slurm-contribs
# --------------

%files contribs
%dir %{_docdir}/%{name}
%dir %{_docdir}/%{name}/contribs
%dir %{_docdir}/%{name}/contribs/lua
%{_docdir}/%{name}/contribs/README
%{_docdir}/%{name}/contribs/lua/proctrack.lua
%{_bindir}/seff
%{_bindir}/sgather
%{_bindir}/sjobexitmod
%{_bindir}/sjstat
%{_bindir}/smail
%{_mandir}/man1/sgather.1*
%{_mandir}/man1/sjobexitmod.1*
%{_mandir}/man1/sjstat.1*

# --------------
# Slurm-openlava
# --------------

%files openlava
%{_bindir}/bjobs
%{_bindir}/bkill
%{_bindir}/bsub
%{_bindir}/lsid
%{_mandir}/man1/bjobs.1*
%{_mandir}/man1/bkill.1*
%{_mandir}/man1/bsub.1*
%{_mandir}/man1/lsid.1*

# -------------
# Slurm-perlapi
# -------------

%files perlapi
%dir %{perl_vendorarch}/Slurm
%dir %{perl_vendorarch}/auto/Slurm
%dir %{perl_vendorarch}/auto/Slurmdb
%{_mandir}/man3/Slurm*.3pm*
%{perl_vendorarch}/Slurm.pm
%{perl_vendorarch}/Slurm/*.pm
%{perl_vendorarch}/Slurmdb.pm
%{perl_vendorarch}/auto/Slurm/Slurm.so
%{perl_vendorarch}/auto/Slurmdb/Slurmdb.so
%{perl_vendorarch}/auto/Slurmdb/autosplit.ix

# ---------------
# Slurm-pam_slurm
# ---------------

%files pam_slurm
%{_libdir}/security/pam_slurm.so
%{_libdir}/security/pam_slurm_adopt.so

# ------------
# Slurm-torque
# ------------

%files torque
%{_bindir}/generate_pbs_nodefile
%{_bindir}/mpiexec
%{_bindir}/pbsnodes
%{_bindir}/qalter
%{_bindir}/qdel
%{_bindir}/qhold
%{_bindir}/qrerun
%{_bindir}/qrls
%{_bindir}/qstat
%{_bindir}/qsub
%{_libdir}/%{name}/job_submit_pbs.so
%{_libdir}/%{name}/spank_pbs.so
%{_mandir}/man1/pbsnodes.1*
%{_mandir}/man1/qalter.1*
%{_mandir}/man1/qdel.1*
%{_mandir}/man1/qhold.1*
%{_mandir}/man1/qrerun.1*
%{_mandir}/man1/qrls.1*
%{_mandir}/man1/qstat.1*
%{_mandir}/man1/qsub.1*
%{_mandir}/man1/mpiexec.1*

%post slurmctld
%systemd_post slurmctld.service

%preun slurmctld
%systemd_preun slurmctld.service

%postun slurmctld
%systemd_postun_with_restart slurmcltd.service

%post slurmd
%systemd_post slurmd.service

%preun slurmd
%systemd_preun slurmd.service

%postun slurmd
%systemd_postun_with_restart slurmd.service

%post slurmdbd
%systemd_post slurmdbd.service

%preun slurmdbd
%systemd_preun slurmdbd.service

%postun slurmdbd
%systemd_postun_with_restart slurmdbd.service

%changelog
* Sat Feb 10 2018 Philip Kovacs <pkdevel@yahoo.com> - 17.11.3-1
- Release of 17.11 series
- Re-aligned rpm packaging to be closer to upstream
- Enabled new slurm native X11 support using ssh2
- Enabled new shared libslurm for smaller code size
- Enabled `check` unit testing via check-devel
- Added environment module support for pmi/slurm
- Add dependency to pmix
- Removed gtk-update-icon-cache scriptlets
- Use new ldconfig_scriptlets macro

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 17.02.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.9-3
- Added patch to enable full relro builds and operation
- Added patch to link knl_generic plugin to libnuma if available
- Remove the following cray or bluegene-only plugins
- job_container/cncu, select/alps, select/bluegene
- Rename slurm_setuser to slurm-setuser
- Minor corrections to slurm.conf

* Wed Nov 1 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.9-2
- Correct desktop categories for rpmgrill.desktop-lint

* Wed Nov 1 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.9-1
- Version bump to close CVE-2017-15566
- Adjusted patches per closure of upstream bug #3942
- Added desktop categories per rpmgrill.desktop-lint

* Wed Oct 25 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.8-1
- Version bump, patches adjusted

* Thu Oct 5 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.7-4
- Patch changes per resolution of upstream bug #4101:
- salloc/sbatch/srun: must be root to use --uid/--gid options
- salloc: supplemental groups dropped after setuid

* Thu Oct 5 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.7-3
- Added BuildRequires gcc and minor packaging conformance items

* Sat Sep 16 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.7-2
- Removed unneeded Requires(pre)

* Thu Sep 14 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.7-1
- Packaging for Fedora
