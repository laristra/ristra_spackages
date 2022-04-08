# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from spack.pkg.builtin.legion import Legion

class Legion(Legion):
    version('cr.11', commit='d857f327975667c92e331328cb6eddf6735c8cf2')
    version('cr.10', commit='f03d00e7d595885040d5c7491160a22fc1dd5ff5')
    version('cr.9', commit='181e63ad4187fbd9a96761ab3a52d93e157ede20')
    version('cr.8', commit='207041b9900ff5adbe13f5b323e82e4d46f38e9c')
    # version('cr.7', commit='363fcbaa27a5239c2e2528309a5333ca6f97425e')
    version('cr.7', commit='7041e61e70a4a041bfee983f2aab9e061c5a6e61', preferred=True)
    version('cr.6', commit='095be5c6e8d36a6ddb235fd079bc6e9b8d37baeb')
    version('cr.5', commit='a204dced578258246ea0933293f4017058bc4bf5')
    version('cr.4', commit='b66083076016c63ea8398fdb89c237880fcb0173')
    version('cr.3', commit='572576b312509e666f2d72fafdbe9d968b1a6ac3')
    version('cr.2', commit='96682fd8aae071ecd30a3ed5f481a9d84457a4b6')
    version('cr.1', commit='a03671b21851d5f0d3f63210343cb61a630f4405')
    version('cr.0', commit='177584e77036c9913d8a62e33b55fa784748759c')

