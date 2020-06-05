#!/bin/bash

display_usage() { 
	echo "This script must be passed three arguments:"
	echo "- The Compiler Module"
	echo "- The spack spec to install against"
	echo "- The name for the module file"
	echo "- And, if not already provided via SPACK_ROOT, the path to the desired spack installation"
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

echo '' | tee ${modName}

# (Re-)Initialize Spack
#export cmd="source ${spackroot}/share/spack/setup-env.sh"
#( echo "$cmd" && $cmd ) | tee ${modName}.log
#source ${spackroot}/share/spack/setup-env.sh

# Get variables from spack
spackarch=`${spackroot}/bin/spack arch`
spackmod="${spackroot}/share/spack/modules/${spackarch}"

echo "spackarch=$spackarch" | tee -a ${modName}.log
echo "spackmod=$spackmod" | tee -a ${modName}.log

# Clean spackage
export cmd="${spackroot}/bin/spack clean --all"
( echo "$cmd" && $cmd ) | tee -a ${modName}.log

# Create spack environment
export cmd="${spackroot}/bin/spack env create ristra_module_gen"
( echo "$cmd" && $cmd ) | tee -a ${modName}.log

# Activate spack environment
export cmd="${spackroot}/bin/spack env activate -p ristra_module_gen"
( echo "$cmd" && $cmd ) | tee -a ${modName}.log

# Install spackage
export cmd="${spackroot}/bin/spack install ${spackSpec}"
( echo "$cmd" && $cmd ) | tee -a ${modName}.log
#spack install ${spackSpec}

# Refresh spackage modules
export cmd="${spackroot}/bin/spack module tcl refresh -y ${spackSpec}"
( echo "$cmd" && $cmd ) | tee -a ${modName}.log

# Generate module load commands
export cmd="${spackroot}/bin/spack module tcl loads --dependencies ${spackSpec}"
( echo "$cmd" ) | tee -a ${modName}.log
( $cmd ) | tee -a ${modName}.log ${modName}
# spack env loads -r

# Deactivate spack environment
export cmd="${spackroot}/bin/spack env deactivate"
( echo "$cmd" && $cmd ) | tee -a ${modName}.log

# Remove spack environment
export cmd="${spackroot}/bin/spack env rm -y ristra_module_gen"
( echo "$cmd" && $cmd ) | tee -a ${modName}.log

# Clean spackage
export cmd="${spackroot}/bin/spack clean --all"
( echo "$cmd" && $cmd ) | tee -a ${modName}.log

# Prepend to module path
sed -i "1s;^;module use ${spackmod}\n;" ${modName}

# And clean up the module path to not overwhelm users with spack
echo "if { [ module-info mode remove ] } { module unuse ${spackmod} }" >> ${modName}

# Add compiler load
sed -i "1s;^;module load ${compiler}\n;" ${modName}

# And add Module shebang(?)
sed -i "1s;^;#%Module\n;" ${modName}

