# Ansbile playbooks and utilities for Batfish

This repository contains utilities and example playbooks showing users how to use Batfish in conjunction with Ansible.


## Playbooks

### Setup

- **batfish_setup.yml**: Retrieves latest Batfish docker image from DockerHub and installs the latest version of Pybatfish along with the other python module requirements. 

### Tutorials

- **bf_tutorial_1.yml**: Shows you how to retrieve facts about network devices

- **bf_tutorial_2.yml**: Shows you how to validate facts about network devices

- **bf_tutorial_3.yml**: Shows you how to validate the routing and forwarding behavior of the network

- **bf_tutorial_4.yml**: Shows you how to validate the behavior of a packet filter(ACL/Firewall rule) 

- **bf_tutorial_5.yml**: Shows you how to validate configuration attributes to find mis-configured BGP sessions and undefined references

## Pre-requisites
- Docker must be installed and running on your machine

- Install the [Batfish role](https://galaxy.ansible.com/batfish/base) from Ansible Galaxy.

  `ansible-galaxy install batfish.base`
  - If you encounter any issues related to SSL certificates use the `-c` option. 
  - When you want to update the role in the future, you will need use the `--force` option.
  
  
- Clone or download this repository to your local machine.


## Playbook invocation

- **Setup Batfish on your local machine**

  This playbook will download the latest Batfish docker container, Pybatfish SDK and other Python requirements and install it on your local machine. It always runs on `localhost`.

  The playbook has some rudimentary error checking built into it:  
  - Aborts if Docker is not running.
  - Warns if it does not detect a Python virtual environment and ask you to confirm that you want to proceed with the installation.
  
  `ansible-playbook -i inventory playbooks/batfish_setup.yml`

- **Run your first Batfish tutorial**

   Batfish is designed to provide complete network analysis, which is why all tasks calling Batfish modules should set `delegate_to: localhost` and `run_once: true`.
   This playbook is setup that way, so you can incorporate non-Batfish tasks that need to run across other hosts in your inventory.

  `ansible-playbook -i inventory playbooks/bf_tutorial_1.yml`

   Each playbook is a standalone tutorial, it does not depend on any playbooks having been run first. So feel free to execute them in whatever order you think is best.
   
## Documentation

Documentation for the Ansible modules can be found [here](https://github.com/batfish/ansible/blob/master/docs/README.md).

Documentation for Batfish can be found [here](https://github.com/batfish/batfish).

