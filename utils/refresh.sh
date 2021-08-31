#!/bin/bash

display_usage() {
        echo "This script assumes update.sh has been run for setup"
        echo "Needs 2 arguments:"
        echo "- The Spack version (e.g. v0.15.3, v0.16.2, etc.)"
        echo "- The Path relative to the current folder that contains spack.yaml (e.g. ristra_spackages/env/x86_64/flecsalemm-deps)"
        echo "Example: ./refresh.sh v0.15.4 ristra_spackages/env/x86_64/flecsalemm-deps" 
}

if [ $# -lt 2 ]
then
        display_usage
        exit 1
fi

version="$1"
spackenvname="$2"

spack_version="spack-${version}"
export SPACK_ROOT=`pwd`/${spack_version}
if [ ! -d ${SPACK_ROOT} ];
then
  echo "${SPACK_ROOT} does not exist!";
  echo "The update.sh script should be run before this script."
  exit 1;
fi
#source ${SPACK_ROOT}/share/spack/setup-env.sh

# Get the <target> based on value of 'spack arch'
spack_arch=`${SPACK_ROOT}/bin/spack arch`
target="${spack_arch##*-}"

# Build packages against x86_64 when it is either 'haswell' or 'skylake_avx512'
# Both are possible Darwin frontend nodes
[ ${target} == "haswell" ] && export target="x86_64"
[ ${target} == "skylake_avx512" ] && export target="x86_64"
export spack_arch=${spack_arch%-*}-${target}

# Refresh spack generated modules
echo 'spack module tcl refresh -y'
${SPACK_ROOT}/bin/spack -e ${spackenvname} module tcl refresh -y

#echo 'Comment out LUA ?.so and etc.' -> achieve by blacklisting the LUA_PATH and LUA_CPATH vars
#for l in ${SPACK_ROOT}/share/spack/modules/${spack_arch}/lua/*;
#do
#  sed -i '/^[^#]/ s/\(^.*prepend-path --delim ";".*$\)/#\ \1/' $l;
#done

# Add 'module load gcc/<version>' in the spack enerated modules
# Spack does not recognize compilers as normal package and thus cannot add compilers automatically
echo 'Add load gcc'
for d in ${SPACK_ROOT}/share/spack/modules/${spack_arch}/*;
do
  if [ -d $d ];
  then
    for f in $d/*;
    do
      if [ -f $f ];
      then
        export temp_f=${f##*/};
        export temp_f2=${temp_f##*gcc-};
        sed -i "s/#%Module1.0/#%Module\nmodule load gcc\/${temp_f2%%-*}\n/" $f;
      else
        echo "Not a file: $f";
      fi
    done
  else
    echo "Not a directory: $d";
    echo "Check your modules.yaml";
  fi
done
