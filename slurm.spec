# -------------
# Base Packages
# -------------
# slurm
# slurm-devel
# slurm-doc
# slurm-gui
# slurm-libs
# slurm-plugins
# slurm-plugins-auth_none
# slurm-plugins-lua
# slurm-plugins-munge
# slurm-plugins-mysql
# slurm-plugins-pbs
# slurm-plugins-rrdtool
# slurm-slurmdbd

# -----------------
# Contribs Packages
# -----------------
# slurm-contribs
# slurm-openlava
# slurm-perlapi
# slurm-plugins-pam_slurm
# slurm-torque

Name:           slurm
Version:        17.02.9
Release:        2%{?dist}
Summary:        Simple Linux Utility for Resource Management
License:        GPLv2 and BSD
URL:            https://slurm.schedmd.com/
Source0:        http://www.schedmd.com/download/latest/%{name}-%{version}.tar.bz2
Source1:        slurm.conf
Source2:        slurmdbd.conf
Source3:        slurm-sview.desktop
Source4:        slurm-128x128.png
Source5:        slurm_setuser.in

# build-related patches
Patch1:         slurm_perlapi_rpaths.patch
Patch2:         slurm_html_doc_path.patch
Patch3:         slurm_doc_fix.patch

# Fedora-related patches
Patch4:         slurm_service_files.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  hdf5-devel
BuildRequires:  pkgconfig(hwloc)
BuildRequires:  pkgconfig(libfreeipmi)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(mariadb)
BuildRequires:  pkgconfig(munge)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pam-devel
BuildRequires:  pmix-devel
BuildRequires:  readline-devel
BuildRequires:  pkgconfig(librrd)
BuildRequires:  pkgconfig(zlib)

# follow arch exclusions for these devel packages
%ifnarch s390 s390x %{arm}
BuildRequires:  libibmad-devel
BuildRequires:  libibumad-devel
BuildRequires:  numactl-devel
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  perl-ExtUtils-MakeMaker
BuildRequires:  perl-podlators
BuildRequires:  pkgconf
%{?systemd_requires}
BuildRequires:  systemd

Requires:       %{name}-plugins%{?_isa} = %{version}-%{release}
Requires:       %{name}-plugins-munge%{?_isa} = %{version}-%{release}
Requires:       munge

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
%description libs
Slurm shared libraries.

%package plugins
Summary: Slurm plugins (loadable shared objects)
%description plugins
Slurm plugins (loadable shared objects) supporting a wide variety of
architectures and behaviors. These basically provide the building blocks
with which Slurm can be configured. Note that some system specific plugins
are in other packages.

%package plugins-auth_none
Summary: Slurm auth null implementation (no authentication)
%description plugins-auth_none
Slurm null authentication plugin.

%package plugins-lua
Summary: Slurm lua plugins
%description plugins-lua
Slurm proctrack/lua and job_submit/lua plugins.

%package plugins-munge
Summary: Slurm authentication and crypto plugins using Munge
%description plugins-munge
Slurm authentication and crypto implementation using Munge. Used to
authenticate user originating an RPC, digitally sign and/or encrypt messages.

%package plugins-mysql
Summary: Slurm MySQL/MariaDb support
%description plugins-mysql
Slurm MySQL/MariaDb support plugins implementing interfaces to those
databases for accounting storage and job completion.

%package plugins-pbs
Summary: Slurm torque (PBS) support
%description plugins-pbs
Slurm torque (PBS) support plugins.

%package plugins-rrdtool
Summary: Slurm rrdtool external sensor plugin
%description plugins-rrdtool
Slurm external sensor plugin for rrdtool. This package is separated from
the base plugins package due to gui dependencies which are unneeded if not
using this plugin.

%package slurmdbd
Summary: Slurm database daemon
# Use with auth_none or munge plugins for authentication
Requires: %{name}-plugins-munge%{?_isa} = %{version}-%{release}
Requires: %{name}-plugins-mysql%{?_isa} = %{version}-%{release}
Requires: munge
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

%package plugins-pam_slurm
Summary: Slurm pam modules
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%description plugins-pam_slurm
The pam_slurm module restricts access to compute nodes in a cluster where Slurm
is in use.  Also includes the pam_slurm_adopt plugin for "adopting" connections
into slurm jobs.

%package torque
Summary: Torque/PBS wrappers for transition from Torque/PBS to Slurm
Requires: %{name}-perlapi%{?_isa} = %{version}-%{release}
Requires: %{name}-plugins-pbs%{?_isa} = %{version}-%{release}
%description torque
Torque wrapper scripts used for helping migrate from Torque/PBS to Slurm.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
cp %SOURCE1 etc/slurm.conf
cp %SOURCE1 etc/slurm.conf.example
cp %SOURCE2 etc/slurmdbd.conf
cp %SOURCE2 etc/slurmdbd.conf.example
mkdir -p share/applications
mkdir -p share/icons/hicolor/128x128/apps
cp %SOURCE3 share/applications/%{name}-sview.desktop
cp %SOURCE4 share/icons/hicolor/128x128/apps/%{name}.png
mkdir -p extras
cp %SOURCE5 extras/slurm_setuser.in

%build
%{__aclocal} -I auxdir
%{__autoconf}
%{__automake} --no-force
# upstream bug #2443.  need to force lazy linkage since plugins contain
# undefined symbols not used in every context, i.e. slurmctld vs slurmd.
CFLAGS="$RPM_OPT_FLAGS -Wl,-z,lazy"
CXXFLAGS="$RPM_OPT_FLAGS -Wl,-z,lazy"
# --enable-debug (auxdir/x_ac_debug.m4) breaks fortification (-O0)
%configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir}/%{name} \
  --with-pam_dir=%{_libdir}/security \
  --enable-shared \
  --disable-static \
  --disable-debug \
  --disable-developer \
  --disable-bluegene \
  --disable-native-cray \
  --disable-cray-network \
  --disable-salloc-background \
  --disable-multiple-slurmd \
  --disable-partial_attach \
  --without-rpath \
# patch libtool to remove rpaths
sed -i 's|^hardcode_into_libs=.*|hardcode_into_libs=no|g' libtool

# configure the extras/slurm_setuser script
sed -r '
s|^dir_conf=.*|dir_conf="%{_sysconfdir}/%{name}"|g;
s|^dir_log=.*|dir_log="%{_var}/log/%{name}"|g;
s|^dir_run=.*|dir_run="%{_rundir}/%{name}"|g;
s|^dir_spool=.*|dir_spool="%{_var}/spool/%{name}"|g;
s|^dir_tmpfiles_d=.*|dir_tmpfiles_d="%{_tmpfilesdir}"|g;' \
    extras/slurm_setuser.in > extras/slurm_setuser

# build base packages
%make_build V=1

# build contribs packages
# INSTALLDIRS=vendor so perlapi goes to vendor_perl directory
PERL_MM_PARAMS="INSTALLDIRS=vendor" %make_build contrib V=1

%check
%{__make} check

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
cat  >%{buildroot}%{_tmpfilesdir}/slurm.conf <<EOF
D %{_rundir}/%{name} 0755 root root -
EOF

# logrotate.d file for /var/log/slurm logging possibilities
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

# pkgconfig file
install -d -m 0755 %{buildroot}%{_libdir}/pkgconfig
cat >%{buildroot}%{_libdir}/pkgconfig/slurm.pc <<EOF
includedir=%{_prefix}/include
libdir=%{_libdir}

Cflags: -I\${includedir}
Libs: -L\${libdir} -lslurm
Description: Slurm API
Name: %{name}
Version: %{version}
EOF

# desktop file for sview GTK+ program
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    share/applications/%{name}-sview.desktop

# desktop icon for sview GTK+ program
install -d -m 0755 %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
install -m 0644 share/icons/hicolor/128x128/apps/%{name}.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# install the extras/slurm_setuser script
install -m 0755 extras/slurm_setuser \
    %{buildroot}%{_bindir}/slurm_setuser

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
# remove example plugins
rm -f %{buildroot}%{_libdir}/%{name}/job_submit_defaults.so
rm -f %{buildroot}%{_libdir}/%{name}/job_submit_logging.so
rm -f %{buildroot}%{_libdir}/%{name}/job_submit_partition.so
# remove bluegene files
rm -f %{buildroot}%{_libdir}/%{name}/libsched_if.so
rm -f %{buildroot}%{_libdir}/%{name}/libsched_if64.so
rm -f %{buildroot}%{_libdir}/%{name}/runjob_plugin.so
rm -f %{buildroot}%{_mandir}/man5/bluegene*
rm -f %{buildroot}%{_sbindir}/sfree
rm -f %{buildroot}%{_sbindir}/slurm_epilog
rm -f %{buildroot}%{_sbindir}/slurm_prolog
# remove cray files
rm -f %{buildroot}%{_libdir}/%{name}/acct_gather_energy_cray.so
rm -f %{buildroot}%{_libdir}/%{name}/core_spec_cray.so
rm -f %{buildroot}%{_libdir}/%{name}/job_submit_cray.so
rm -f %{buildroot}%{_libdir}/%{name}/select_cray.so
rm -f %{buildroot}%{_libdir}/%{name}/switch_cray.so
rm -f %{buildroot}%{_libdir}/%{name}/task_cray.so
rm -f %{buildroot}%{_mandir}/man5/cray*
# remove percs files
rm -f %{buildroot}%{_libdir}/%{name}/launch_poe.so
rm -f %{buildroot}%{_libdir}/%{name}/libpermapi.so
rm -f %{buildroot}%{_libdir}/%{name}/switch_nrt.so
# remove perl cruft
rm -f %{buildroot}%{perl_vendorarch}/auto/Slurm*/.packlist
rm -f %{buildroot}%{perl_vendorarch}/auto/Slurm*/Slurm*.bs
rm -f %{buildroot}%{perl_archlib}/perllocal.pod

# filter unneeded dependencies
%global __requires_exclude ^libpmix.so|libevent

# -----
# Slurm
# -----

%files
%doc CONTRIBUTING.md DISCLAIMER META NEWS README.rst RELEASE_NOTES
%license COPYING LICENSE.OpenSSL
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/layouts.d
%{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/cgroup*.conf
%{_sysconfdir}/%{name}/cgroup*.conf.example
%config(noreplace) %{_sysconfdir}/%{name}/slurm.conf
%{_sysconfdir}/%{name}/slurm.conf.example
%{_sysconfdir}/%{name}/layouts.d/*.example
%attr(0755,root,root) %{_sysconfdir}/%{name}/slurm.epilog.clean
%dir %{_rundir}/%{name}
%ghost %{_rundir}/%{name}/slurmctld.pid
%ghost %{_rundir}/%{name}/slurmd.pid
%{_bindir}/{sacct,sacctmgr,salloc,sattach,sbatch,sbcast}
%{_bindir}/{scancel,scontrol,sdiag,sh5util,sinfo,sprio}
%{_bindir}/{squeue,sreport,srun,sshare,sstat,strigger}
%{_bindir}/slurm_setuser
%{_unitdir}/slurmctld.service
%{_unitdir}/slurmd.service
%{_tmpfilesdir}/slurm.conf
%{_sbindir}/slurmctld
%{_sbindir}/slurmd
%{_sbindir}/slurmstepd
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
%{_mandir}/man8/slurmctld.8*
%{_mandir}/man8/slurmd.8*
%{_mandir}/man8/slurmstepd.8*
%{_mandir}/man8/spank.8*
%dir %{_var}/log/%{name}
%dir %{_var}/spool/%{name}
%dir %{_var}/spool/%{name}/ctld
%dir %{_var}/spool/%{name}/d

# -----------
# Slurm-devel
# -----------

%files devel
%dir %{_prefix}/include/%{name}
%{_prefix}/include/%{name}/pmi*.h
%{_prefix}/include/%{name}/slurm.h
%{_prefix}/include/%{name}/slurm_errno.h
%{_prefix}/include/%{name}/slurmdb.h
%{_prefix}/include/%{name}/smd_ns.h
%{_prefix}/include/%{name}/spank.h
%{_libdir}/libpmi*.so
%{_libdir}/libslurm.so
%{_libdir}/libslurmdb.so
%{_libdir}/pkgconfig/%{name}.pc
%dir %{_libdir}/%{name}/src
%dir %{_libdir}/%{name}/src/sattach
%{_libdir}/%{name}/src/sattach/sattach.wrapper.c
%dir %{_libdir}/%{name}/src/srun
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
%{_libdir}/libpmi*.so.*
%{_libdir}/libslurm.so.*
%{_libdir}/libslurmdb.so.*

# -------------
# Slurm-plugins
# -------------

%files plugins
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/accounting_storage_{filetxt,none,slurmdbd}.so
%{_libdir}/%{name}/acct_gather_energy_{ibmaem,ipmi,none,rapl}.so
%{_libdir}/%{name}/acct_gather_filesystem_{lustre,none}.so
%{_libdir}/%{name}/acct_gather_infiniband_{none,ofed}.so
%{_libdir}/%{name}/acct_gather_profile_{hdf5,none}.so
%{_libdir}/%{name}/burst_buffer_generic.so
%{_libdir}/%{name}/checkpoint_{none,ompi}.so
%{_libdir}/%{name}/core_spec_none.so
%{_libdir}/%{name}/crypto_openssl.so
%{_libdir}/%{name}/ext_sensors_none.so
%{_libdir}/%{name}/gres_{gpu,mic,nic}.so
%{_libdir}/%{name}/job_container_{cncu,none}.so
%{_libdir}/%{name}/job_submit_all_partitions.so
%{_libdir}/%{name}/job_submit_require_timelimit.so
%{_libdir}/%{name}/job_submit_throttle.so
%{_libdir}/%{name}/jobacct_gather_{cgroup,linux,none}.so
%{_libdir}/%{name}/jobcomp_{elasticsearch,filetxt,none,script}.so
%{_libdir}/%{name}/launch_slurm.so
%{_libdir}/%{name}/layouts_power_{cpufreq,default}.so
%{_libdir}/%{name}/layouts_unit_default.so
%{_libdir}/%{name}/mcs_{account,group,none,user}.so
%{_libdir}/%{name}/mpi_{lam,mpich1_p4,mpich1_shmem,mpichgm,mpichmx}.so
%{_libdir}/%{name}/mpi_{mvapich,none,openmpi,pmi2,pmix,pmix_v1}.so
%{_libdir}/%{name}/node_features_knl_generic.so
%{_libdir}/%{name}/power_none.so
%{_libdir}/%{name}/preempt_{job_prio,none,partition_prio,qos}.so
%{_libdir}/%{name}/priority_{basic,multifactor}.so
%{_libdir}/%{name}/proctrack_{cgroup,linuxproc,pgid}.so
%{_libdir}/%{name}/route_{default,topology}.so
%{_libdir}/%{name}/sched_{backfill,builtin,hold}.so
%{_libdir}/%{name}/select_{alps,bluegene,cons_res,linear,serial}.so
%{_libdir}/%{name}/slurmctld_nonstop.so
%{_libdir}/%{name}/switch_{generic,none}.so
%{_libdir}/%{name}/task_{affinity,cgroup,none}.so
%{_libdir}/%{name}/topology_{3d_torus,hypercube,node_rank,none,tree}.so

# -----------------------
# Slurm-plugins-auth_none
# -----------------------

%files plugins-auth_none
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/auth_none.so

# -----------------
# Slurm-plugins-lua
# -----------------

%files plugins-lua
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/job_submit_lua.so
%{_libdir}/%{name}/proctrack_lua.so

# -------------------
# Slurm-plugins-munge
# -------------------

%files plugins-munge
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/auth_munge.so
%{_libdir}/%{name}/crypto_munge.so

# -------------------
# Slurm-plugins-mysql
# -------------------

%files plugins-mysql
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/accounting_storage_mysql.so
%{_libdir}/%{name}/jobcomp_mysql.so

# -----------------
# Slurm-plugins-pbs
# -----------------

%files plugins-pbs
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/job_submit_pbs.so
%{_libdir}/%{name}/spank_pbs.so

# ---------------------
# Slurm-plugins-rrdtool
# ---------------------

%files plugins-rrdtool
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/ext_sensors_rrd.so

# --------
# Slurmdbd
# --------

%files slurmdbd
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/slurmdbd.conf
%{_sysconfdir}/%{name}/slurmdbd.conf.example
%dir %{_rundir}/%{name}
%ghost %{_rundir}/%{name}/slurmdbd.pid
%{_bindir}/slurm_setuser
%{_unitdir}/slurmdbd.service
%{_tmpfilesdir}/slurm.conf
%{_sbindir}/slurmdbd
%{_mandir}/man5/slurmdbd.conf.5*
%{_mandir}/man8/slurmdbd.8*

# --------------
# Slurm-contribs
# --------------

%files contribs
%{_bindir}/seff
%{_bindir}/sgather
%{_bindir}/sjobexitmod
%{_bindir}/sjstat
%{_bindir}/smail
%{_mandir}/man1/sgather.1*
%{_mandir}/man1/sjobexitmod.1*
%{_mandir}/man1/sjstat.1*
%dir %{_docdir}/%{name}
%dir %{_docdir}/%{name}/contribs
%{_docdir}/%{name}/contribs/README
%dir %{_docdir}/%{name}/contribs/lua
%{_docdir}/%{name}/contribs/lua/proctrack.lua

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
%{perl_vendorarch}/Slurm.pm
%dir %{perl_vendorarch}/Slurm
%{perl_vendorarch}/Slurm/*.pm
%{perl_vendorarch}/Slurmdb.pm
%dir %{perl_vendorarch}/auto/Slurm
%{perl_vendorarch}/auto/Slurm/Slurm.so
%dir %{perl_vendorarch}/auto/Slurmdb
%{perl_vendorarch}/auto/Slurmdb/Slurmdb.so
%{perl_vendorarch}/auto/Slurmdb/autosplit.ix
%{_mandir}/man3/Slurm*.3pm*

# ---------------
# Slurm-pam_slurm
# ---------------

%files plugins-pam_slurm
%dir %{_libdir}/%{name}
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
%{_mandir}/man1/pbsnodes.1*
%{_mandir}/man1/qalter.1*
%{_mandir}/man1/qdel.1*
%{_mandir}/man1/qhold.1*
%{_mandir}/man1/qrerun.1*
%{_mandir}/man1/qrls.1*
%{_mandir}/man1/qstat.1*
%{_mandir}/man1/qsub.1*
%{_mandir}/man1/mpiexec.1*

%post
%systemd_post slurmd.service
%systemd_post slurmctld.service

%preun
%systemd_preun slurmd.service
%systemd_preun slurmctld.service

%postun
%systemd_postun_with_restart slurmd.service
%systemd_postun_with_restart slurmctld.service

%post devel -p /sbin/ldconfig

%postun devel -p /sbin/ldconfig

%post gui
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gui
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gui
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post slurmdbd
%systemd_post slurmdbd.service

%preun slurmdbd
%systemd_preun slurmdbd.service

%postun slurmdbd
%systemd_postun_with_restart slurmdbd.service

%changelog
* Wed Nov 1 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.9-2
- Correct desktop categories for rpmgrill.desktop-lint.

* Wed Nov 1 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.9-1
- Version bump to close CVE-2017-15566.
- Adjusted patches per closure of upstream bug #3942.
- Added desktop categories per rpmgrill.desktop-lint.

* Wed Oct 25 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.8-1
- Version bump, patches adjusted.

* Thu Oct 5 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.7-4
- Patch changes per resolution of upstream bug #4101:
- salloc/sbatch/srun: must be root to use --uid/--gid options.
- salloc: supplemental groups dropped after setuid.

* Thu Oct 5 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.7-3
- Added BuildRequires gcc and minor packaging conformance items.

* Sat Sep 16 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.7-2
- Removed unneeded Requires(pre).

* Thu Sep 14 2017 Philip Kovacs <pkdevel@yahoo.com> - 17.02.7-1
- Packaging for Fedora.
