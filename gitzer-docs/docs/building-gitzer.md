---
id: building-gitzer
title: Building Gitzer
---

## The build script

The source repository has a [script](https://github.com/IgnisDa/Gitzer/blob/main/tools/build-gitzer)
which is used to build the tar file that is posted on the
[releases page](https://github.com/IgnisDa/Gitzer/releases). Simply run it in the root of
the source code to obtain the final tar file. The script assumes that the gitzer source
directory is in `~/Gitzer` (which it should be if you are using the Vagrant method of
development).

```bash
./tools/build-gitzer
```

## Naming convention

The final output of the above command will be `gitzer-${version}.tar.gz` where the value of
`$version` is read from the [`VERSION`](https://github.com/IgnisDa/Gitzer/blob/main/VERSION)
file present in the project root.
