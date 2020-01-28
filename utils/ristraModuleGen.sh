#!/bin/bash

display_usage() { 
	echo "This script must be passed three arguments:"
	echo "- The Compiler Module"
	echo "- The spack spec to install against"
	echo "- The name for the module file"
	echo "- And, if not already provided via SPACK_ROOT, the path to the desired spack installation"
	echo "e.g. ./ristraModuleGen.sh gcc/8.2.0 flecsalemm-deps+caliper%gcc@8.2.0 flecsalemm-deps-gcc-8.2.0-withCaliper" 
        echo "Note: if there are/will be more than one version of a certain package installed through spack, full specification of the package will be necessary to avoid multiple 'module load' of the same package under different variations."
} 

if [ $# -lt 3 ] 
then
	display_usage
	exit 1
fi

compiler="$1"
spackSpec="$2"
modName="$3"
spackroot=""

if [ -z "$SPACK_ROOT" ]
then
	if [ $# -lt 4 ]
	then
		display_usage
		exit 1
	fi
	spackroot="$4"
else
	spackroot="$SPACK_ROOT"
fi

# (Re-)Initialize Spack
source ${spackroot}/share/spack/setup-env.sh


# Get variables from spack
spackarch=`spack arch`
spackmod="${spackroot}/share/spack/modules/${spackarch}"

# Install spackage
spack install ${spackSpec}

# Generate module load commands
spack module tcl loads  --dependencies ${spackSpec} | tee ${modName}

# Prepend to module path
sed -i "1s;^;module use ${spackmod}\n;" ${modName}

# And clean up the module path to not overwhelm users with spack
echo "if { [ module-info mode remove ] } { module unuse ${spackmod} }" >> ${modName}

# Add compiler load
sed -i "1s;^;module load ${compiler}\n;" ${modName}

# And add Module shebang(?)
sed -i "1s;^;#%Module\n;" ${modName}

