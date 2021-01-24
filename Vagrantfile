# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Set the base box used to build the image
  config.vm.box = "bento/ubuntu-20.10"
  # Name of the machine that is created
  config.vm.host_name = "gitzer-development"
  # Network settings and port forwarding
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "0.0.0.0"
  config.vm.network "forwarded_port", guest: 3000, host: 3000, host_ip: "0.0.0.0"
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "0.0.0.0"
  config.vm.network "forwarded_port", guest: 8534, host: 8534, host_ip: "0.0.0.0"
  config.vm.network "forwarded_port", guest: 8533, host: 8533, host_ip: "0.0.0.0"
  # This folder is synced to the machine
  config.vm.synced_folder ".", "/home/vagrant/Gitzer"
  # VirtualBox is the default provider, and we specify some specific settings here
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "2048"
    vb.cpus = "2"
  end
  # This script sets up python3, npm, yarn, postgresql etc.
  config.vm.provision :shell, :path => "tools/Vagrant/bootstrap"
  # This script installs each specific application's dependencies
  config.vm.provision :shell, :path => "tools/Vagrant/setup-deps", privileged: false
  # This script sets some environment variables that are essential to development
  # This is done by adding a custom script to /etc/profile.d/
  config.vm.provision :shell, :path => "tools/shell/env-vars"
end
