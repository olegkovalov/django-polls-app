# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.box = "boxcutter/ubuntu1604" # Ubuntu 16.04
  config.vm.box_version = "<=2.0.18"

  config.vm.network "forwarded_port", guest: 80, host: 8080  # nginx

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
    vb.cpus = 2
    vb.customize ["modifyvm", :id, "--ioapic", "on"]
  end

  config.vm.provision "ansible" do |ansible|
    ansible.playbook = "provisioning/server.yml"
    ansible.extra_vars = { ansible_ssh_user: "vagrant"}
    ansible.raw_arguments = ['-e env=vagrant']
  end

end
