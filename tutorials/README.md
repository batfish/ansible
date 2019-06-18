# Tutorials for the batfish.base role

This repository contains example playbooks that show how to use Batfish in conjunction with Ansible.

- [tutorial1_extract_facts.yml](playbooks/tutorial1_extract_facts.yml): Shows how to retrieve facts about network devices

- [tutorial2_validate_facts.yml](playbooks/tutorial2_validate_facts.yml): Shows how to validate facts about network devices

- [tutorial3_validate_forwarding.yml](playbooks/tutorial3_validate_forwarding.yml): Shows how to validate the routing and forwarding behavior of the network

- [tutorial4_validate_acls.yml](playbooks/tutorial4_validate_acls.yml): Shows how to validate the behavior of a packet filter(ACL/Firewall rule) 

- [tutorial5_validate_bgp_sessions.yml](playbooks/tutorial5_validate_bgp_sessions.yml): Shows how to validate configuration attributes to find mis-configured BGP sessions and undefined references

- [bf_upload_diagnostics.yml](playbooks/bf_upload_diagnostics.yml): Shows how to upload diagnostic information about your snapshot in the event of issues (e.g. if Batfish fails to fully recognized some lines in your input files)

## Setup

- Ensure that Docker is installed and running on your machine.

- Install the latest version of the `batfish.base` role from Ansible Galaxy.

  `ansible-galaxy install --force batfish.base`
  - If you encounter any issues related to SSL certificates use the `-c` option. 

- Clone or download this repository to your local machine, and run the setup playblook.

- Setup Batfish on your local machine

  `cd tutorials`

  `ansible-playbook -i inventory playbooks/batfish_setup.yml`

  This playbook will download and install the latest Batfish docker container, Pybatfish SDK and other Python requirements. It has some rudimentary error checking built into it:  
  - Aborts if Docker is not running.
  - Warns if it does not detect a Python virtual environment and ask you to confirm that you want to proceed with the installation.
  

## Running a tutorial

We highly recommend that you run the tutorials in a Python 3 virtual environment. Details on how to set one up can be found [here](https://docs.python.org/3/library/venv.html).

From the `tutorials` directory, run specific tutorials via

  `ansible-playbook -i inventory playbooks/tutorial1_extract_facts.yml`

   Each playbook is a standalone tutorial, it does not depend on other tutorials having been run first. So feel free to execute them in whatever order you think is best.

   Batfish is designed to provide complete network analysis, which is why all tasks calling Batfish modules should set `delegate_to: localhost` and `run_once: true`. The tutorials are set up that way, so you can incorporate non-Batfish tasks that need to run across other hosts in your inventory.


## Documentation

 - [Documentation for the Ansible modules](../docs/README.md)

 - [Documentation for Batfish](https://github.com/batfish/batfish)

