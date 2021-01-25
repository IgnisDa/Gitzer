---
id: installing
title: Getting Gitzer
sidebar_label: Installing
slug: /
---

## Installing Gitzer

Gitzer provides a custom installer that will install gitzer isolated from the rest of your
system by vendorizing its dependencies. This is the recommended way of installing Gitzer.

```bash
curl -sSL https://raw.githubusercontent.com/IgnisDa/Gitzer/main/get-gitzer.py | python
# OR on UBUNTU
curl -sSL https://raw.githubusercontent.com/IgnisDa/Gitzer/main/get-gitzer.py | python3
```

## Uninstalling Gitzer

Gitzer can be completely uninstalled from your system by running the get-gitzer.py script
with the -u flag.

```bash
curl -sSL https://raw.githubusercontent.com/IgnisDa/Gitzer/main/get-gitzer.py -o get-gitzer.py
python get-gitzer.py --uninstall
# OR on UBUNTU
python3 get-gitzer.py --uninstall
```
