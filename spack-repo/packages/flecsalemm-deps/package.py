# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os

class FlecsalemmDeps(BundlePackage):
    '''TODO
    '''
    homepage ='https://github.com/laristra/flecsale'
    git = 'https://github.com/laristra/flecsale.git'

    version('master', branch='master', submodules=False)

    variant('backend', default='mpi', values=('mpi', 'legion', 'hpx'),
            description='Backend to use for distributed memory', multi=False)
    variant('debug_backend', default=False,
            description='Build Backend with Debug Mode')
    variant('doxygen', default=False,
        description='Enable doxygen')
    variant('hdf5', default=True,
            description='Enable HDF5 Support')
    variant('caliper', default=False,
            description='Enable Caliper Support')
    variant('graphviz', default=False,
            description='Enable GraphViz Support')
    variant('tutorial', default=False,
            description='Build FleCSI Tutorials')
    variant('flecstan', default=False,
        description='Build FleCSI Static Analyzer')
    variant('cinch', default=False,
        description='Enable External Cinch')
    variant('trilinos', default=False,
            description='Enable Trilinos Support')

    for b in ['mpi', 'legion', 'hpx']:
        depends_on("flecsi-deps backend=%s" % b,
            when="backend=%s" % b)
    for v in ['debug_backend', 'doxygen', 'hdf5', 'caliper', 'graphviz', 'tutorial', 'flecstan', 'cinch']:
        depends_on("flecsi-deps +%s" % v, when="+%s" % v)
        depends_on("flecsi-deps ~%s" % v, when="~%s" % v)


    depends_on('pkgconfig', type='build')
    depends_on('cmake@3.12:')
    #depends_on('charmpp backend=mpi', when='backend=charm++')
    depends_on('boost@1.70.0: cxxstd=14 +program_options')
    depends_on('metis@5.1.0:')
    depends_on('parmetis@4.0.3:')
    depends_on('trilinos@12.12.1:12.14.1~alloptpkgs+amesos~amesos2+anasazi+aztec+belos+boost~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+hdf5+hypre+ifpack~ifpack2~intrepid~intrepid2~isorropia~kokkos+metis~minitensor+ml+muelu+mumps+nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos~tpetra~x11~xsdkflags~zlib+zoltan~zoltan2', when='+trilinos')
    depends_on('gotcha')
    depends_on('eospac@6.4.0:')
    depends_on('exodusii')
    depends_on('random123')
    depends_on('hypre')
    depends_on('lua@5.3.5')
    depends_on('netcdf-c@4.7.0:')
    # Not actually a flecaslemm-dep but related to fixing dependency/trilinos issues
    depends_on('suite-sparse@:5.3.0', when='+trilinos')
    # May come from netcdf but not seeming to propagate correctly on all platforms
    depends_on('hdf5+hl', when='+hdf5')

    def setup_run_environment(self, env):
        if '+hdf5' in self.spec:
            env.set('HDF5_ROOT', self.spec['hdf5'].prefix)
