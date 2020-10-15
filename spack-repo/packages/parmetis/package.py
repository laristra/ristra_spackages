# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from spack.pkg.builtin.parmetis import Parmetis

class Parmetis(Parmetis):

    variant('int64', default=False, description='Sets the bit width of METIS\'s index type to 64.')

    depends_on('metis+int64', when='+int64')
    depends_on('metis~int64', when='~int64')

