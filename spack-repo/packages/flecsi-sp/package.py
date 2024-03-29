# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class FlecsiSp(CMakePackage):
    '''Flecsi-SP contains various specializations for use with the FleCSI core programming system.
    '''
    git = "ssh://git@gitlab.lanl.gov/laristra/flecsi-sp.git"

    version('1.4', branch='1.4', submodules=False, preferred=True)

    variant('backend', default='mpi', values=('serial', 'mpi', 'legion', 'charmpp', 'hpx'),
            description='Backend to use for distributed memory', multi=False)
    variant('debug_backend', default=False,
            description='Build Backend with Debug Mode')
    variant('external_cinch', default=True,
            description='Enable External Cinch')
    variant('shared', default=True,
            description='Build shared libraries')
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
    variant('portage', default=False,
            description='Enable Portage Support')


    for b in ['mpi', 'legion', 'hpx']:
        depends_on("flecsi@1.4 backend=%s" % b,
            when="backend=%s" % b)
    for v in ['debug_backend', 'external_cinch', 'shared', 'doxygen', 'hdf5', 'graphviz', 'tutorial']:
        depends_on("flecsi@1.4 +%s" % v, when="+%s" % v)
        depends_on("flecsi@1.4 ~%s" % v, when="~%s" % v)
    depends_on("flecsi@1.4 caliper_detail=low", when='+caliper')

    depends_on('libristra')
    depends_on('cmake@3.12:')
    # Requires cinch > 1.0 due to cinchlog installation issue
    depends_on('cinch@1.01:', type='build', when='+external_cinch')
    depends_on('exodusii@2016-08-09')
    depends_on('hdf5+hl+mpi', when='+hdf5')

    #portage requires LAPACKE
    depends_on('netlib-lapack lapacke=true', when='+portage')


    def cmake_args(self):
        spec = self.spec
        options = []

        if '+external_cinch' in spec:
            options.append('-DCINCH_SOURCE_DIR=' + spec['cinch'].prefix)

        if self.run_tests:
            options.append('-DENABLE_UNIT_TESTS=ON')
        else:
            options.append('-DENABLE_UNIT_TESTS=OFF')

        if spec.variants['backend'].value == 'legion':
            options.append('-DFLECSI_RUNTIME_MODEL=legion')
            options.append('-DENABLE_MPI=ON')
        elif spec.variants['backend'].value == 'mpi':
            options.append('-DFLECSI_RUNTIME_MODEL=mpi')
            options.append('-DENABLE_MPI=ON')
        elif spec.variants['backend'].value == 'hpx':
            options.append('-DFLECSI_RUNTIME_MODEL=hpx')
            options.append('-DENABLE_MPI=ON')
        elif spec.variants['backend'].value == 'charmpp':
            options.append('-DFLECSI_RUNTIME_MODEL=charmpp')
            options.append('-DENABLE_MPI=ON')
        else:
            options.append('-DFLECSI_RUNTIME_MODEL=serial')
            options.append('-DENABLE_MPI=OFF')

        return options

#    def setup_run_environment(self, env):
#        env.set('EXODUSII_ROOT', self.spec['exodusii'].prefix)
#        env.prepend_path('CMAKE_PREFIX_PATH',self.spec['flecsi'].prefix.cmake.flecsi)
#        env.prepend_path('CMAKE_PREFIX_PATH',self.spec['libristra'].prefix.cmake.libristra)
