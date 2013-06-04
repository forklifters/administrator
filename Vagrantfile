# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  # Every Vagrant virtual environment requires a box to build off of.
  config.vm.box = "precise32"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  config.vm.box_url = "http://files.vagrantup.com/precise32.box"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  config.vm.network :forwarded_port, guest: 80, host: 8000

  # Provisioning
  # config.vm.provision :shell, :path => "bootstrap.sh"
  config.vm.provision :shell, :inline => "sudo apt-get update && sudo apt-get install -y puppet"

  config.vm.provision :puppet do |puppet|
      puppet.manifests_path = "manifests"
      puppet.manifest_file  = "base.pp"
  end

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  config.vm.network :private_network, ip: "33.33.33.33"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network :public_network

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "~/", "/home/host"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  # config.vm.provider :virtualbox do |vb|
  #   # Don't boot with headless mode
  #   vb.gui = true
  #
  #   # Use VBoxManage to customize the VM. For example to change memory:
  #   vb.customize ["modifyvm", :id, "--memory", "1024"]
  # end

  config.vm.provider :aws do |aws, override|
    override.vm.box = 'dummy'
    override.vm.box_url = "https://github.com/mitchellh/vagrant-aws/raw/master/dummy.box"

    #aws.ami = 'ami-de0d9eb7'
    #aws.instance_type = 't1.micro'
    aws.ami = "ami-7747d01e"

    aws.security_groups = ['vagrant'] # Currently this causes an exception

    override.ssh.username = "ubuntu"
  end

  # View the documentation for the provider you're using for more
  # information on available options.

end
