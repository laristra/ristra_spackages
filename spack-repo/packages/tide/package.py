from spack import *

class Tide(CMakePackage):
    '''tide is a Lua library to assist with initializing FleCSI-based
applications by providing source code generation for some of the
compile-time configuration required by FleCSI.'''

    homepage = ""
    git      = "git@gitlab.lanl.gov:laristra/tide"

    version("0.2.0", tag="v0.2.0", submodules=False, preferred=True)
    version("0.1.0", tag="v0.1.0", submodules=False)


    variant("shared_lua", default=False,
            description="Build with shared lua")

    depends_on("cmake@3.15.0:", type="build")
    depends_on("llvm@10:")
    depends_on("lua@5.3.0:5.3.999~shared", when="~shared_lua")
    depends_on("lua@5.3.0:5.3.999+shared", when="+shared_lua")
