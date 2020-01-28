# Ristra Spackages

This repository contains the custom spackage files for the repos in laristra family.

## Basic Usage

We assume the user wish to work in the home directory and already have a spack instance setup.

To get the content of this repo 
```
$ git clone git@gitlab.lanl.gov:laristra/ristra_spackages.git
```

To use the custom spackage files with your spack 
```
$ spack repo add ristra_spackages/spack-repo
==> Added repo with namespace 'lanl_ristra'.

$ spack repo list
==> 2 package repositories.
lanl_ristra        /home/<user>/ristra_spackages/spack-repo
builtin            /home/<user>/spack/var/spack/repos/builtin
```

[Optional]
To ensure you have this custom repo in your spack all the time, move the `repos.yaml` into your spack config folder
```
$ mv /home/<user>/.spack/linux/repos.yaml /home/<user>/spack/etc/spack/
```

Please see the [Spack documentation](https://spack.readthedocs.io/en/latest/configuration.html) for detailed info.
