#!/bin/bash

#Pull compiler from command line
modcompiler=""
spackcompiler=""
namecompiler=""

if [ "$1" == "gcc" ]; then
	modcompiler="gcc/8.2.0"
	spackcompiler="gcc@8.2.0"
	namecompiler="gcc-8.2.0"
else
	echo "Unsupported Toolchain Requested. Currently supported list [gcc]"
fi

# Get variables from spack
spackarch=`spack arch`
spackmod="${SPACK_ROOT}/share/spack/modules/${spackarch}"

# Install spackage
spack install flecsalemm-deps%${spackcompiler}

# Generate module load commands
spack module tcl loads  --dependencies flecsalemm-deps%gcc@8.2.0 | tee flecsalemm-deps-${namecompiler}

# Prepend to module path
sed -i "1s;^;prepend-path MODULEPATH ${spackmod}\n;" flecsalemm-deps-${namecompiler}

# And clean up the module path to not overwhelm users with spack
echo "remove-path MODULEPATH ${spackmod}" >> flecsalemm-deps-${namecompiler}

# Add compiler load
sed -i "1s;^;module load ${modcompiler}\n;" flecsalemm-deps-${namecompiler}

# And add Module shebang(?)
sed -i "1s;^;#%Module\n;" flecsalemm-deps-${namecompiler}

