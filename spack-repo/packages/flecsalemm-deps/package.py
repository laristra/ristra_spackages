# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os

class FlecsalemmDeps(Package):
    """TODO
    """
    homepage ="https://xcp-stash.lanl.gov/projects/LARISTRA/repos/flecsale-mm"
    git      = "ssh://git@xcp-stash.lanl.gov:7999/laristra/flecsale-mm.git"

    version('master', branch='master', submodules=False)

    variant('build_type', default='Release', values=('Debug', 'Release'),
            description='The build type to build', multi=False)
    variant('backend', default='mpi', values=('serial', 'mpi', 'legion', 'charm++', 'hpx'),
            description='Backend to use for distributed memory', multi=False)
    variant('debug_backend', default=False,
            description='Build Backend with Debug Mode')
    variant('shared', default=True,
            description='Build shared libraries')
    variant('hdf5', default=False,
            description='Enable HDF5 Support')
    variant('caliper', default=False,
            description='Enable Caliper Support')
    variant('graphviz', default=False,
            description='Enable GraphViz Support')
    variant('tutorial', default=False,
            description='Build FleCSI Tutorials')

    depends_on("pkgconfig", type='build')
    depends_on("cmake@3.1:")
    depends_on('mpi', when='backend=mpi')
    depends_on('mpi', when='backend=legion')
    depends_on('mpi', when='backend=hpx')
    depends_on('legion@ctrl-rep-3 +shared +mpi +hdf5', when='backend=legion +hdf5')
    depends_on('legion@ctrl-rep-3 +shared +mpi', when='backend=legion ~hdf5')
    depends_on('charmpp backend=mpi', when='backend=charm++')
    depends_on('hpx@1.3.0 cxxstd=14', when='backend=hpx')
    depends_on('boost@1.70.0: cxxstd=14 +program_options')
    depends_on("metis@5.1.0:")
    depends_on("parmetis@4.0.3:")
    depends_on('hdf5', when='+hdf5')
    depends_on('caliper', when='+caliper')
    depends_on('graphviz', when='+graphviz')
    depends_on('python@3.0:', when='+tutorial')
    depends_on("trilinos@12.12.1:12.14.1 ~alloptpkgs+amesos~amesos2+anasazi+aztec+belos+boost~cgns~complex~dtk+epetra+epetraext+exodus+explicit_template_instantiation~float+fortran~fortrilinos+gtest+hdf5+hypre+ifpack~ifpack2~intrepid~intrepid2~isorropia~kokkos+metis~minitensor+ml+muelu+mumps+nox~openmp~phalanx~piro~pnetcdf~python~rol~rythmos+sacado~shards+shared~stk+suite-sparse~superlu~superlu-dist~teko~tempus+teuchos~tpetra~x11~xsdkflags~zlib+zoltan~zoltan2")
    depends_on("gotcha")
    depends_on("eospac")
    depends_on("exodusii")
    depends_on("random123")
    depends_on("hypre")
    depends_on("lua@5.3.5")
    # Not actually a flecaslemm-dep but related to fixing dependency/trilinos issues
    depends_on("suite-sparse@:5.3.0")

    # Dummy install for now,  will be removed when metapackage is available
    def install(self, spec, prefix):
        with open(os.path.join(spec.prefix, 'package-list.txt'), 'w') as out:
            for dep in spec.dependencies(deptype='build'):
                out.write("%s\n" % dep.format(
                    format_string='${PACKAGE} ${VERSION}'))
                os.symlink(dep.prefix, os.path.join(spec.prefix, dep.name))
            out.close()
