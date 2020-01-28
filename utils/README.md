# Ristra Spackages Utils

This folder contains utility scripts.

## ristraModuleGen.sh

This script takes compiler, spack specification of desired package, output module name, and optionally the SPACK_ROOT path as input arguments to install any missing dependencies through spack and then generate a module file for desired package that contains all necessary dependencies.

Note: If SPACK_ROOT is not set in the environment nor given to the script, the script assumes the desired spack instance has already been setup by user and ready to go.

If you don't have a spack instance setup, you could reference the setup below. 

However, do note that we are assuming we need the spackage files in this repo, the configs in ristra-spack-configurations and mirrors in the ngc project space.

We assume the user wish to work in the home directory.

First, you need to download Spack if you don't already have one.
```
$ git clone https://github.com/spack/spack.git
```

Second, you need this repo for the custom spackage files if you haven't clone yet.
```
$ git clone git@gitlab.lanl.gov:laristra/ristra_spackages.git
```
Then add a `repos.yaml` in `/home/<user>/spack/etc/spack/linux` folder 
```
$ mkdir -p /home/<user>/spack/etc/spack/linux
$ vim /home/<user>/spack/etc/spack/linux/repos.yaml
```
with the following content
```
repos:
- /home/<user>/ristra_spackages/spack-repo
```

Third, you need the spack compilers and packages config files if you don't want to make one yourself.
```
$ git clone git@gitlab.lanl.gov:laristra/ristra-spack-configurations.git
```
Then copy the config files under the right platform into your spack instance's config folder
```
$ cp /home/<user>/ristra-spack-configurations/<platform>/* /home/<user>/spack/etc/spack/linux/
```

Fourth, you need the spack mirrors from the ngc space if you don't want to download the source every time for every packages by adding a `mirrors.yaml` in `/home/<user>/spack/etc/spack/linux`
```
$ vim /home/<user>/spack/etc/spack/linux/mirrors.yaml
```
with the following content.
```
mirrors:
  flecsalemm-deps: file:///usr/projects/ngc/public/ristra_spack_mirrors/flecsalemm-deps-mirror
```

Now you can invoke the script like such
```
$ /home/<user>/ristra_spackages/utils/ristraModuleGen.sh gcc/8.3.0 "flecsalemm-deps%gcc@8.3.0 backend=mpi ^mpich@3.2.1%gcc@8.3.0+slurm" "flecsalemm-deps_2020.01.27-backend_mpi-mpich_3.2.1-gcc_8.3.0" "/home/<user>/spack"
```

