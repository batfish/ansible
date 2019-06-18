#!/usr/bin/env bash
set -euxo pipefail

BUILDKITE_DIR="$(dirname "${BASH_SOURCE[0]}")"
source ${BUILDKITE_DIR}/setup_ansible.sh

pushd tutorials

pip freeze

# Run tutorial setup
# Build essential is required to build regex python dependency...
sudo apt-get update
sudo apt-get install build-essential
ansible-playbook -i inventory --extra-vars "batch_mode=true" playbooks/batfish_setup.yml

pip freeze

# Run the tutorial
ansible-playbook -i inventory playbooks/tutorial1_extract_facts.yml
