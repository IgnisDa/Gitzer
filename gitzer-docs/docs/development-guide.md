---
id: development-guide
title: Development environment installation
---

## Cloning the repository

The project [source code](https://github.com/IgnisDa/Gitzer) is hosted on Github. To
get started, fork the repository and then clone it to your local development machine.

```bash
git clone --config pull.rebase https://github.com/~your-username~/Gitzer.git
```

## Installing Vagrant

The main development for Gitzer occurs using [Vagrant](https://www.vagrantup.com/) and
all the associated scripts to setup a development environment for Gitzer are already present
in the repository.

You can install Vagrant from [here](https://www.vagrantup.com/downloads). Once you have
downloaded it, you can verify your installation using `vagrant --version`. At the time
of writing this guide, the output of that command is `Vagrant 2.2.14`. You might have to
restart your machine after installing Vagrant.

## Starting the virtual machine

Once you have verified your installation, you can start the provisioning of the machine
with the following command:

```bash
vagrant up
```

Typically, provisioning can take anywhere from 10 to 15 minutes.

## Verification

If all went well, you should have a functioning development environment now. To verify,
run `vagrant ssh` in the project root. This will directly drop you into a terminal
session of the machine that you just provisioned. Run the following commands to verify
if it works correctly.

```bash
cd ~/Gitzer
./tools/run-dev
```

Open up your browser and visit `http://127.0.0.1:8000/` to access the backend development
server powered by Django. Visit `http://127.0.0.1:3000/` to access the frontend development
server powered by NuxtJs.

:::tip

The `run-dev` script doesn't start up the documentation development server by default.
To launch that, run the following commands:

```bash
cd ~/Gitzer/gitzer-docs
yarn start
```

Then visit `http://127.0.0.1:8080/` in your web browser to access the documentation
development server powered by Docusaurus.
:::
