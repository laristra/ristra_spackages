#!/bin/bash

display_usage() { 
	echo "This script will update spack, ristra-spack-configurations, ristra_spackages and flecsalemm-deps mirror or clone/create them if any of them doesn't already exist in the executing folder"
        echo "Needs 3 arguments:"
	echo "- The Spack version (e.g. v0.14.2, v0.15.3, etc.)"
	echo "- The System (e.g. Darwin, Snow, Trinitite, etc.)"
        echo "- The Spackage name for creating mirror (e.g. flecsalemm-deps)"
	echo "Example: ./update.sh v0.15.3 Darwin flecsalemm-deps" 
} 

if [ $# -lt 3 ] 
then
	display_usage
	exit 1
fi

spack_version="spack-$1"
system="$2"
packagename="$3"

export SPACK_ROOT=`pwd`/${spack_version}
if [ ${packagename} == "ristra-deps" ];
then
  export mirror=`pwd`/ristra_spack_mirrors/${packagename}-mirror;
elif [ ${packagename} == "flecsalemm-deps" ];
then
  export mirror=`pwd`/ristra_spack_mirrors/${packagename}-mirror;
else
  export mirror=`pwd`/ristra_spack_mirrors_pro/${packagename}-mirror;
fi

[ ! -d "${SPACK_ROOT}" ] && { git clone https://github.com/spack/spack.git; mv spack ${spack_version}; cd ${spack_version}; git init --shared=group . ; git checkout ${spack_version##*-}; cd ..; }

spack_arch=`${SPACK_ROOT}/bin/spack arch`
platform="${spack_arch%%-*}"

echo 'Update ristra-spack-configurations'
[ ! -d "ristra-spack-configurations" ] && git clone git@gitlab.lanl.gov:laristra/ristra-spack-configurations.git
cd ristra-spack-configurations
git init --shared=group .
git pull
cd ..

echo "Clean up ${spack_version}/etc/spack/${platform} and ${spack_version}/etc/spack"
mkdir -p ${spack_version}/etc/spack/${platform}
rm -rf ${spack_version}/etc/spack/${platform}/*.yaml
rm -rf ${spack_version}/etc/spack/*.yaml

# Copy configs from ristra-spack-configurations' common folder and <system> folder within the <spack_config_version_folder>
# Also, copy configs from private/pro folder under the <system>/<spack_config_version_folder> when applicable
echo "Copy ristra-spack-configurations/${platform}/*.yaml into ${spack_version}/etc/spack/${platform}"
cp ristra-spack-configurations/common/*.yaml ${spack_version}/etc/spack/
if [ -d ristra-spack-configurations/${system}/${1%.*} ];
then
  spack_config_version_folder="${1%.*}";
else
  echo "WARNING: Specified version cannot be found; Defaulting to the latest for deployment purpose";
  spack_config_version_folder="latest";
fi
cp ristra-spack-configurations/${system}/${spack_config_version_folder}/*.yaml ${spack_version}/etc/spack/${platform}/
[ ${packagename} == "flecsalemm-deps" ] && cp ristra-spack-configurations/${system}/${spack_config_version_folder}/public/*.yaml ${spack_version}/etc/spack/${platform}/
[ ${packagename} == "symphony-deps" ] && cp ristra-spack-configurations/${system}/${spack_config_version_folder}/private/*.yaml ${spack_version}/etc/spack/${platform}/

# Checks if the spack in upstreams.yaml exists
# Remove the upstreams.yaml if not
if [ -f "${SPACK_ROOT}/etc/spack/${platform}/upstreams.yaml" ];
then
  export spack_modules=`awk '/tcl/{print $NF}' ${SPACK_ROOT}/etc/spack/${platform}/upstreams.yaml`;
  export spack_modules_array=($spack_modules);
  for s in "${!spack_modules_array[@]}"; do [ ! -d ${spack_modules_array[s]} ] && { rm ${SPACK_ROOT}/etc/spack/${platform}/upstreams.yaml; break; }; done
fi

# HPC mirror has cached an older version of flecsi and cinch
${SPACK_ROOT}/bin/spack mirror rm --scope site lanl

echo 'Update ristra_spackages'
[ ! -d "ristra_spackages" ] && git clone git@gitlab.lanl.gov:laristra/ristra_spackages.git
cd ristra_spackages
git init --shared=group .
git pull
cd ..
${SPACK_ROOT}/bin/spack repo add --scope site ristra_spackages/spack-repo || /bin/true

if [ ${packagename} == "symphony-deps" ];
then
  [ ! -d "ristra_spackages_pro" ] && git clone git@gitlab.lanl.gov:laristra/ristra_spackages_pro.git;
  cd ristra_spackages_pro;
  git init --shared=group . ;
  git pull;
  cd .. ;
  ${SPACK_ROOT}/bin/spack repo add --scope site ristra_spackages_pro/spack-repo || /bin/true;
fi

echo "Update ${mirror}"
mkdir -p ${mirror}
[ ${packagename} == "ristra-deps" ] && export packagename=flecsalemm-deps;

${SPACK_ROOT}/bin/spack mirror create -d ${mirror} --dependencies ${packagename}+hdf5+caliper+trilinos%gcc backend=legion ^mpich@3.2.1+slurm
${SPACK_ROOT}/bin/spack mirror create -d ${mirror} --dependencies ${packagename}+doxygen+graphviz+portage+paraview%gcc backend=hpx ^openmpi@3.1.4
#${SPACK_ROOT}/bin/spack mirror add --scope site ${packagename} "file://${mirror}"
