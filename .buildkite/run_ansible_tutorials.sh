#!/usr/bin/env bash
set -euxo pipefail

source setup_ansible.sh

# Run tutorial setup
ansible-playbook -i inventory playbooks/batfish_setup.yml

# Run the tutorial
ansible-playbook -i inventory playbooks/tutorial1_extract_facts.yml
