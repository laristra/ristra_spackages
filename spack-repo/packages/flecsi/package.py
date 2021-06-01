# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

class Flecsi(CMakePackage):
    '''FleCSI is a compile-time configurable framework designed to support
       multi-physics application development. As such, FleCSI attempts to
       provide a very general set of infrastructure design patterns that can
       be specialized and extended to suit the needs of a broad variety of
       solver and data requirements. Current support includes multi-dimensional
       mesh topology, mesh geometry, and mesh adjacency information,
       n-dimensional hashed-tree data structures, graph partitioning
       interfaces,and dependency closures.
    '''
    homepage = 'http://flecsi.org/'
    git      = 'https://github.com/flecsi/flecsi.git'

    version('develop', branch='devel', submodules=False)
    version('1', git="https://github.com/laristra/flecsi.git", branch='1', submodules=False, preferred=False)
    version('1.4', git="https://github.com/laristra/flecsi.git",  branch='1.4', submodules=False, preferred=True)

    variant('backend', default='mpi', values=('serial', 'mpi', 'legion', 'hpx', 'charmpp'),
            description='Backend to use for distributed memory', multi=False)
    variant('debug_backend', default=False,
            description='Build Backend with Debug Mode')
    variant('minimal', default=False,
            description='Disable FindPackageMetis')
    variant('shared', default=True,
            description='Build shared libraries')
    variant('flog', default=False,
            description='Enable flog testing')
    variant('doxygen', default=False,
            description='Enable doxygen')
    variant('doc', default=False,
            description='Enable documentation')
    variant('coverage', default=False,
            description='Enable coverage build')
    variant('hdf5', default=True,
            description='Enable HDF5 Support')
    variant('caliper_detail', default='none',
            values=('none', 'low', 'medium', 'high'),
            description='Set Caliper Profiling Detail', multi=False)
    variant('graphviz', default=False,
            description='Enable GraphViz Support')
    variant('tutorial', default=False,
            description='Build FleCSI Tutorials')
    variant('flecstan', default=False,
            description='Build FleCSI Static Analyzer')
    variant('external_cinch', default=True,
            description='Enable External Cinch')
    variant('kokkos', default=False,
            description='Enable Kokkos Support')
    variant('unit_tests', default=False,
            description='Build with Unit Tests Enabled')

    # All Current FLecsi Releases
    for level in ('low', 'medium', 'high'):
        depends_on('caliper', when='caliper_detail=%s' % level)
        depends_on('caliper@2.0.1~adiak', when='@:1.9 caliper_detail=%s' % level)
    depends_on('graphviz', when='+graphviz')
    depends_on('hdf5+mpi', when='+hdf5')
    depends_on('metis@5.1.0:')
    depends_on('parmetis@4.0.3:')

    # Flecsi@1.x
    depends_on('cmake@3.12:', when='@:1.9')
    # Requires cinch > 1.0 due to cinchlog installation issue
    depends_on('cinch@1.01:', type='build', when='+external_cinch @:1.9')
    depends_on('mpi', when='backend=mpi @:1.9')
    depends_on('mpi', when='backend=legion @:1.9')
    depends_on('mpi', when='backend=hpx @:1.9')
    depends_on('legion+shared+mpi', when='backend=legion @:1.9')
    depends_on('legion+hdf5', when='backend=legion +hdf5 @:1.9')
    depends_on('legion build_type=Debug', when='backend=legion +debug_backend @:1.9')
    depends_on('hpx@1.4.1 cxxstd=17 malloc=system max_cpu_count=128', when='backend=hpx @:1.9')
    depends_on('hpx build_type=Debug', when='backend=hpx +debug_backend @:1.9')
    depends_on('boost@1.70.0: cxxstd=17 +program_options', when='@:1.9')
    depends_on('googletest@1.8.1+gmock', when='@:1.9')
    depends_on('hdf5+hl+mpi', when='+hdf5 @:1.9')
    depends_on('python@3.0:', when='+tutorial @:1.9')
    depends_on('doxygen', when='+doxygen @:1.9')
    depends_on('llvm', when='+flecstan @:1.9')
    depends_on('pfunit@3.0:3.99', when='@:1.9')
    depends_on('py-gcovr', when='+coverage @:1.9')

    # Flecsi@2.x
    depends_on('cmake@3.15:', when='@2.0:')
    depends_on('boost@1.70.0 cxxstd=17 +program_options +atomic +filesystem +regex +system', when='@2.0:')
    depends_on('graphviz', when='+graphviz @2.0:')
    depends_on('kokkos@3.2.00:', when='+kokkos @2.0:')
    depends_on('legion@ctrl-rep-9:ctrl-rep-99',when='backend=legion @2.0:')
    depends_on('legion+hdf5',when='backend=legion +hdf5 @2.0:')
    depends_on('hdf5@1.10.7:',when='backend=legion +hdf5 @2.0:')
    depends_on('hpx@1.3.0 cxxstd=17 malloc=system',when='backend=hpx @2.0:')
    depends_on('kokkos@3.2.00:', when='+kokkos @2.0:')
    depends_on('mpich@3.4.1', when='@2.0: ^mpich')
    depends_on('openmpi@4.1.0', when='@2.0: ^openmpi')



    conflicts('+tutorial', when='backend=hpx')
    # Flecsi@2: no longer supports serial or charmpp backends
    conflicts('backend=serial', when='@2.0:')
    conflicts('backend=charmpp', when='@2.0:')
    # FLecsi@2: no longer expects to control how backend is built
    conflicts('+debug_backend', when='@2.0:')
    # Flecsi@2: No longer supports previous TPL related flags
    conflicts('+minimal', when='@2.0:')
    # Flecsi@2: no longer provides documentation variants
    conflicts('+doxygen', when='@2.0:')
    conflicts('+doc', when='@2.0:')
    # Flecsi@2: no longer provides coverage variants
    conflicts('+coverage', when='@2.0:')
    # Flecsi@2: no longer provides tutorial variants
    conflicts('+tutorial', when='@2.0:')
    # Flecsi@2: no longer supports flecstan
    conflicts('+flecstan', when='@2.0:')
    # Flecsi@2: integrates cinch and no longer depends on external installs
    conflicts('+external_cinch', when='@2.0:')
    # Current Flecsi@:1.9 releases do not support kokkos
    conflicts('+kokkos', when='@:1.9')
    # Unit tests require flog support
    conflicts('+unit_tests', when='~flog')

    def cmake_args(self):
        #TODO: Add a big switch on version because of course
        spec = self.spec
        options = ['-DENABLE_OPENMP=ON',
                   '-DCXX_CONFORMANCE_STANDARD=c++17',
                   '-DENABLE_METIS=ON',
                   '-DENABLE_PARMETIS=ON',
                   '-DENABLE_COLORING=ON',
                   '-DENABLE_DEVEL_TARGETS=ON'
                   ]

        if '+cinch' in spec:
            options.append('-DCINCH_SOURCE_DIR=' + spec['cinch'].prefix)


        if spec.variants['backend'].value == 'legion':
            options.append('-DFLECSI_RUNTIME_MODEL=legion')
            options.append('-DENABLE_MPI=ON')
        elif spec.variants['backend'].value == 'mpi':
            options.append('-DFLECSI_RUNTIME_MODEL=mpi')
            options.append('-DENABLE_MPI=ON')
        elif spec.variants['backend'].value == 'hpx':
            options.append('-DFLECSI_RUNTIME_MODEL=hpx')
            options.append('-DENABLE_MPI=ON')
            options.append('-DHPX_IGNORE_CMAKE_BUILD_TYPE_COMPATIBILITY=ON')
        elif spec.variants['backend'].value == 'charmpp':
            options.append('-DFLECSI_RUNTIME_MODEL=charmpp')
            options.append('-DENABLE_MPI=ON')
        else:
            options.append('-DFLECSI_RUNTIME_MODEL=serial')
            options.append('-DENABLE_MPI=OFF')

        if self.run_tests:
            options.append('-DENABLE_UNIT_TESTS=ON')
        else:
            options.append('-DENABLE_UNIT_TESTS=OFF')

        if '+minimal' in spec:
            options.append('-DCMAKE_DISABLE_FIND_PACKAGE_METIS=ON')
        else:
            options.append('-DCMAKE_DISABLE_FIND_PACKAGE_METIS=OFF')
        if '+shared' in spec:
            options.append('-DBUILD_SHARED_LIBS=ON')
        else:
            options.append('-DBUILD_SHARED_LIBS=OFF')

        if '+hdf5' in spec and spec.variants['backend'].value != 'hpx':
            options.append('-DENABLE_HDF5=ON')
        else:
            options.append('-DENABLE_HDF5=OFF')
        if '+caliper' in spec:
            options.append('-DENABLE_CALIPER=ON')
        else:
            options.append('-DENABLE_CALIPER=OFF')
        if '+tutorial' in spec:
            options.append('-DENABLE_FLECSIT=ON')
            options.append('-DENABLE_FLECSI_TUTORIAL=ON')
        else:
            options.append('-DENABLE_FLECSIT=OFF')
            options.append('-DENABLE_FLECSI_TUTORIAL=OFF')

        if '+flecstan' in spec:
            options.append('-DENABLE_FLECSTAN=ON')
        else:
            options.append('-DENABLE_FLECSTAN=OFF')

        if '+doxygen' in spec:
            options.append('-DENABLE_DOXYGEN=ON')
        else:
            options.append('-DENABLE_DOXYGEN=OFF')
        if '+doc' in spec:
            options.append('-DENABLE_DOCUMENTATION=ON')
        else:
            options.append('-DENABLE_DOCUMENTATION=OFF')
        if '+coverage' in spec:
            options.append('-DENABLE_COVERAGE_BUILD=ON')
        else:
            options.append('-DENABLE_COVERAGE_BUILD=OFF')

        return options

