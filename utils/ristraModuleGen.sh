#!/bin/bash

display_usage() { 
	echo "This script must be passed three arguments:"
	echo "- The Compiler Module"
	echo "- The spack spec to install against"
	echo "- And the name for the module file"
	echo "e.g. ./ristraModuleGen.sh gcc/8.2.0 flecsalemm-deps+caliper%gcc@8.2.0 flecsalemm-deps-gcc-8.2.0-withCaliper" 
} 

if [ $# -lt 3 ] 
then
	display_usage
	exit 1
fi

compiler="$1"
spackSpec="$2"
modName="$3"


# Get variables from spack
spackarch=`spack arch`
spackmod="${SPACK_ROOT}/share/spack/modules/${spackarch}"

# Install spackage
spack install ${spackSpec}

# Generate module load commands
spack module tcl loads  --dependencies ${spackSpec} | tee ${modName}

# Prepend to module path
sed -i "1s;^;prepend-path MODULEPATH ${spackmod}\n;" ${modName}

# And clean up the module path to not overwhelm users with spack
echo "remove-path MODULEPATH ${spackmod}" >> ${modName}

# Add compiler load
sed -i "1s;^;module load ${compiler}\n;" ${modName}

# And add Module shebang(?)
sed -i "1s;^;#%Module\n;" ${modName}

