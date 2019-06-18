#!/usr/bin/env bash
set -euxo pipefail

BUILDKITE_DIR="$(dirname "${BASH_SOURCE[0]}")"
source ${BUILDKITE_DIR}/setup_ansible.sh

pushd tutorials

# Run tutorial setup
ansible-playbook -i inventory --extra-vars "batch_mode=true" playbooks/batfish_setup.yml

# Run the tutorial
ansible-playbook -i inventory playbooks/tutorial1_extract_facts.yml
