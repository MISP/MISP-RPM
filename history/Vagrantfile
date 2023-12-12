
# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

BOX = "generic/rhel7"
MISP_RPM_VERSION = "2.4.159-1"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	config.vm.define "misp-rhel7.localhost" do |vmconfig|
		vmconfig.vm.box = BOX
		vmconfig.vm.hostname = "misp-rhel7"
		vmconfig.vm.provision :shell, inline: "wget -O - https://github.com/MISP/MISP-RPM/archive/refs/tags/#{MISP_RPM_VERSION}.tar.gz | sudo -u vagrant tar -zxvf -"
	end
end
