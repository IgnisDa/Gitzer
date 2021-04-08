---
id: details
title: Details
---

## How Gitzer works

### Downloading

When a user runs the
[`get-gitzer.py`](https://github.com/IgnisDa/Gitzer/blob/main/get-gitzer.py)
installation script, the [latest release](https://github.com/IgnisDa/Gitzer/releases/latest)
is downloaded and then unzipped to a temporary directory. This folder is then copied to
`~/gitzer` and the necessary git aliases are set.

### Running

Gitzer depends on a number of [packages](https://github.com/IgnisDa/Gitzer/blob/main/gitzer/requirements.txt)
and these dependencies are vendorized along with the release itself. All these dependencies
can be found in `~/gitzer/_vendor/` directory.

When the user runs `git gitzer`, the command executed is `python3 /home/vagrant/gitzer/main.py`.
The dependencies have to be added to `PYTHONPATH` manually since there is no easy way to
activate a virtual environment using python. This is done by
[modifying](https://github.com/IgnisDa/Gitzer/blob/main/tools/main.py#L24) the `sys.path`
variable.
