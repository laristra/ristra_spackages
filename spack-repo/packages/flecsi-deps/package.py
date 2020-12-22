# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

class FlecsiDeps(BundlePackage):
    '''TODO
    '''
    homepage = 'http://flecsi.org/'
    git      = 'https://github.com/laristra/flecsi.git'

    version('devel', branch='devel', submodules=False)
    version('1', branch='1', submodules=False)
    version('1.4', branch='1.4', submodules=False, preferred=True)

    variant('build_type', default='Release',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'),
            description='The build type to build', multi=False)
    variant('backend', default='mpi', values=('mpi', 'legion', 'hpx'),
            description='Backend to use for distributed memory', multi=False)
    variant('debug_backend', default=False,
            description='Build Backend with Debug Mode')
    variant('doxygen', default=False,
            description='Enable doxygen')
    variant('coverage', default=False,
            description='Enable coverage build')
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

    depends_on('cmake@3.12:')
    # Requires cinch > 1.0 due to cinchlog installation issue
    depends_on('cinch@1.01:', type='build', when='+cinch')
    depends_on('mpi', when='backend=mpi')
    depends_on('mpi', when='backend=legion')
    depends_on('mpi', when='backend=hpx')
    depends_on('legion+shared+mpi', when='backend=legion')
    depends_on('legion+hdf5', when='backend=legion +hdf5')
    depends_on('legion build_type=Debug', when='backend=legion +debug_backend')
    depends_on('hpx@1.4.1 cxxstd=17 malloc=system max_cpu_count=128', when='backend=hpx')
    depends_on('hpx build_type=Debug', when='backend=hpx +debug_backend')
    depends_on('boost@1.70.0: cxxstd=17 +program_options')
    depends_on('metis@5.1.0:')
    depends_on('parmetis@4.0.3:')
    depends_on('googletest@1.8.1+gmock')
    depends_on('hdf5+hl+mpi', when='+hdf5')
    depends_on('caliper@2.0.1~adiak', when='+caliper')
    depends_on('graphviz', when='+graphviz')
    depends_on('python@3.0:', when='+tutorial')
    depends_on('doxygen', when='+doxygen')
    depends_on('llvm', when='+flecstan')
    depends_on('pfunit@3.0:3.99')
    depends_on('py-gcovr', when='+coverage')

    conflicts('+tutorial', when='backend=hpx')
