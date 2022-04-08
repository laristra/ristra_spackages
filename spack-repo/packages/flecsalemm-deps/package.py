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
    variant('paraview', default=False,
            description='Build Paraview Support')
    variant('external_cinch', default=True,
        description='Enable External Cinch')
    variant('int64', default=False,
        description='Enable Metis/ParMetis int64 Support')
    variant('trilinos', default=False,
            description='Enable Trilinos Support')
    variant('portage', default=False,
            description='Add Some Portage Dependencies')
    variant('shared_lua', default=False,
            description='Build with shared lua')
    variant('tide', default=False,
            description='Build with tide support')

    depends_on("flecsi-sp@1.4")
    depends_on("flecsi @1:1.9")
    for b in ['mpi', 'legion', 'hpx']:
        depends_on("flecsi-sp backend=%s" % b,
            when="backend=%s" % b)
        depends_on("flecsi backend=%s" % b,
            when="backend=%s" % b)

    for v in ['debug_backend', 'doxygen', 'hdf5', 'graphviz', 'tutorial', 'external_cinch']:
        depends_on("flecsi-sp +%s" % v, when="+%s" % v)
        depends_on("flecsi-sp ~%s" % v, when="~%s" % v)
        depends_on("flecsi +%s" % v, when="+%s" % v)
        depends_on("flecsi ~%s" % v, when="~%s" % v)
    depends_on("flecsi-sp@1.4 +caliper", when='+caliper')
    depends_on("flecsi@1.4 caliper_detail=low", when='+caliper')

    depends_on('pkgconfig', type='build')
    depends_on('cmake@3.12:')
    #depends_on('charmpp backend=mpi', when='backend=charm++')
    depends_on('boost@1.70.0: cxxstd=17 +program_options')
    depends_on('metis@5.1.0:')
    depends_on('parmetis@4.0.3:')
    depends_on('metis+int64@5.1.0:', when='+int64')
    depends_on('parmetis+int64@4.0.3:', when='+int64')
    depends_on('trilinos@12.12.1:12.14.1+amesos~amesos2+anasazi+aztec+belos+boost~complex~dtk+epetra+epetraext~exodus+explicit_template_instantiation~float+fortran+hdf5+hypre+ifpack~ifpack2~intrepid~intrepid2~isorropia~kokkos~minitensor+ml+mumps+nox~openmp~phalanx~piro~python~rol~rythmos+sacado~shards~stk+suite-sparse~superlu~superlu-dist~teko~tempus~tpetra~x11+zoltan~zoltan2~gtest', when='+trilinos')
    depends_on('gotcha')
    depends_on('eospac@6.4.0:')
    depends_on('exodusii')
    depends_on('random123')
    depends_on('hypre')
    depends_on('lua@5.3.5~shared', when='~shared_lua')
    depends_on('lua@5.3.5+shared', when='+shared_lua')
    depends_on('netcdf-c@4.7.0:')
    depends_on('portage-deps', when='+portage')
    # Not actually a flecaslemm-dep but related to fixing dependency/trilinos issues
    depends_on('paraview@5.7.0: +python3+osmesa', when='+paraview')
    depends_on('suite-sparse@:5.3.0', when='+trilinos')
    # May come from netcdf but not seeming to propagate correctly on all platforms
    depends_on('hdf5+hl', when='+hdf5')
    # make sure tide and sphinx are installed for downstream project usage
    depends_on('tide@0.2.0', when='+tide')
    depends_on('py-sphinx@3.0.0:', when='+tide')

    def setup_run_environment(self, env):
        if '+hdf5' in self.spec:
            env.set('HDF5_ROOT', self.spec['hdf5'].prefix)
        env.set('EXODUSII_ROOT', self.spec['exodusii'].prefix)
