#!/usr/bin/env bash
set -euxo pipefail

BUILDKITE_DIR="$(dirname "${BASH_SOURCE[0]}")"
source ${BUILDKITE_DIR}/setup_python.sh
source ${BUILDKITE_DIR}/setup_ansible.sh

pushd tutorials

pip freeze

# Run docker setup
ansible-playbook -i inventory playbooks/batfish_docker_setup.yml

pip freeze

# Run the tutorial
ansible-playbook -i inventory playbooks/tutorial1_extract_facts.yml
