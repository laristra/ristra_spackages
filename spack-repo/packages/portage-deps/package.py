# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os

class PortageDeps(BundlePackage):
    """TODO
    """
    homepage = "https://gitlab.lanl.gov/laristra/portage"
    git      = "ssh://git@gitlab.lanl.gov:laristra/portage.git"

    version('master', branch='master', submodules=False)

    depends_on("cmake@3.13:")
    depends_on("thrust@1.8.3")
    depends_on("netlib-lapack+lapacke@3.8.0")
