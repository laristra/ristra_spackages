#!/bin/bash

display_usage() {
        echo "This script assumes update.sh has been run for setup"
        echo "Needs 3 arguments:"
        echo "- The Spack version (e.g. v0.14.2, v0.15.3, etc.)"
        echo "- The Path where symlink module should be made (e.g. /usr/projects/ngc/private/modulefiles)"
        echo "- The module name (e.g. flecsalemm-deps)"
        echo "Example: ./deploy.sh v0.15.3 /usr/projects/ngc/private/modulefiles flecsalemm-deps" 
}

if [ $# -lt 3 ]
then
        display_usage
        exit 1
fi

version="$1"
modulefiles="$2"
modulename="$3"

spack_version="spack-${version}"
export SPACK_ROOT=`pwd`/${spack_version}
if [ ! -d ${SPACK_ROOT} ];
then
  echo "${SPACK_ROOT} does not exist!";
  echo "The update.sh script should be run before this script."
  exit 1;
fi
#source ${SPACK_ROOT}/share/spack/setup-env.sh

spack_arch=`${SPACK_ROOT}/bin/spack arch`
target="${spack_arch##*-}"
platform="${spack_arch%%-*}"

[ ${target} == "haswell" ] && export target="x86_64"
[ ${target} == "skylake_avx512" ] && export target="x86_64"
export spack_arch=${spack_arch%-*}-${target}

echo 'Concretizing...'
[ ${modulename} == "ristra-deps" ] && ${SPACK_ROOT}/bin/spack -e ristra_spackages/env/${target}/flecsalemm-deps concretize -f
[ ${modulename} == "flecsalemm-deps" ] && ${SPACK_ROOT}/bin/spack -e ristra_spackages/env/${target}/${modulename} concretize -f
[ ${modulename} == "symphony-deps" ] && ${SPACK_ROOT}/bin/spack -e ristra_spackages_pro/env/${target}/${modulename} concretize -f

echo 'spack install -y --show-log-on-error'
[ ${modulename} == "ristra-deps" ] && ${SPACK_ROOT}/bin/spack -e ristra_spackages/env/${target}/flecsalemm-deps install -y --show-log-on-error --only dependencies
[ ${modulename} == "flecsalemm-deps" ] && ${SPACK_ROOT}/bin/spack -e ristra_spackages/env/${target}/${modulename} install -y --show-log-on-error
[ ${modulename} == "symphony-deps" ] && ${SPACK_ROOT}/bin/spack -e ristra_spackages_pro/env/${target}/${modulename} install -y --show-log-on-error

echo 'Running refresh.sh'
[ ${modulename} == "ristra-deps" ] && ./ristra_spackages/utils/refresh.sh ${version} ristra_spackages/env/${target}/flecsalemm-deps
[ ${modulename} == "flecsalemm-deps" ] && ./ristra_spackages/utils/refresh.sh ${version} ristra_spackages/env/${target}/${modulename}
[ ${modulename} == "symphony-deps" ] && ./ristra_spackages/utils/refresh.sh ${version} ristra_spackages_pro/env/${target}/${modulename}

#echo 'Symlink modulefiles'
#mkdir -p ${modulefiles} && cd ${modulefiles} && mkdir -p ${spack_arch} && cd ${spack_arch}
#[ ! -f "${modulename}" ] && ln -s ${SPACK_ROOT}/share/spack/modules/${spack_arch}/${modulename}

mkdir -p ${modulefiles}
cd ${modulefiles}
[ ${modulename} == "ristra-deps" ] && export topmodulename="${spack_arch}-${version}-public"
[ ${modulename} == "flecsalemm-deps" ] && export topmodulename="${spack_arch}-${version}"
[ ${modulename} == "symphony-deps" ] && export topmodulename="${spack_arch}-${version}-pro"
if [ ! -f "${topmodulename}" ];
then
#for f in ${modulename}/*;
#do
  [ -f "${SPACK_ROOT}/etc/spack/${platform}/upstreams.yaml" ] && { export spack_modules=`awk '/tcl/{print $NF}' ${SPACK_ROOT}/etc/spack/${platform}/upstreams.yaml`; export spack_modules_array=($spack_modules); }

  echo 'Create top-level modulefile';
  echo "# This is auto-generated from script." >>  ${topmodulename};

  # And clean up the module path to not overwhelm users with spack
  #echo "if { [ module-info mode remove ] } { module unuse ${SPACK_ROOT}/share/spack/modules/${spack_arch} }" >> ${topmodulename};
  sed -i "1s;^;module use \$module_dir\n;" ${topmodulename};
  [ ${modulename} != "ristra-deps" ] && [ -f "${SPACK_ROOT}/etc/spack/${platform}/upstreams.yaml" ] && { for i in "${!spack_modules_array[@]}"; do sed -i "1s;^;module use \$${i}_module_dir\n;" ${topmodulename}; done }
  sed -i "1s;^;# module use\n;" ${topmodulename};

  # And add module help
  sed -i "1s;^;}\n\n;" ${topmodulename};
  sed -i "1s;^;  puts stderr \"After loading - perform a module avail to present additional modules.\\\\n\"\n;" ${topmodulename};
  sed -i "1s;^;  puts stderr \"is added to the list of directories that the module command will search.\\\\n\"\n;" ${topmodulename};
  sed -i "1s;^;  puts stderr \"\\t\$module_dir \\\\n\"\n;" ${topmodulename};
  [ ${modulename} != "ristra-deps" ] && [ -f "${SPACK_ROOT}/etc/spack/${platform}/upstreams.yaml" ] && { for i in "${!spack_modules_array[@]}"; do sed -i "1s;^;  puts stderr \"\\t\$${i}_module_dir \\\\n\"\n;" ${topmodulename}; done }
  sed -i "1s;^;  puts stderr \"This category contains modules for $spack_arch on this cluster.\\\\n\"\n;" ${topmodulename};
  sed -i "1s;^;global user_moddir\n;" ${topmodulename};
  sed -i "1s;^;proc ModulesHelp { } {\n;" ${topmodulename};
  sed -i "1s;^;# module help\n;" ${topmodulename};

  # And add module whatis
  sed -i "1s;^;module-whatis   \"Loading this module will allow other modules for this category to be presented.\"\n\n;" ${topmodulename};
  sed -i "1s;^;module-whatis   \"\$module_dir. Add this directory to MODULEPATH.\"\n;" ${topmodulename};
  [ ${modulename} != "ristra-deps" ] && [ -f "${SPACK_ROOT}/etc/spack/${platform}/upstreams.yaml" ] && { for i in "${!spack_modules_array[@]}"; do sed -i "1s;^;module-whatis   \"\$${i}_module_dir. Add this directory to MODULEPATH.\"\n;" ${topmodulename}; done }
  sed -i "1s;^;module-whatis   \"Modules for $spack_arch are maintained in\"\n;" ${topmodulename};
  sed -i "1s;^;# module whatis\n;" ${topmodulename};

  # And add module path var
  sed -i "1s;^;set module_dir ${SPACK_ROOT}/share/spack/modules/${spack_arch}\n\n;" ${topmodulename};
  [ ${modulename} != "ristra-deps" ] && [ -f "${SPACK_ROOT}/etc/spack/${platform}/upstreams.yaml" ] && { for i in "${!spack_modules_array[@]}"; do sed -i "1s;^;set ${i}_module_dir ${spack_modules_array[i]}/${spack_arch}\n;" ${topmodulename}; done }

  # And add Module shebang(?)
  sed -i "1s;^;#%Module\n\n;" ${topmodulename};
#done
fi
