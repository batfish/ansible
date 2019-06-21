#!/usr/bin/env bash
set -euxo pipefail

BUILDKITE_DIR="$(dirname "${BASH_SOURCE[0]}")"
source ${BUILDKITE_DIR}/setup_python.sh
source ${BUILDKITE_DIR}/setup_ansible.sh

pushd tutorials

# Run setup playbook
ansible-playbook -i inventory --extra-vars "batch_mode=True" playbooks/batfish_setup.yml

# Run the tutorial assertions playbook, validating the output of the tutorials
ansible-playbook -i inventory tests/e2e/test_tutorials.yml
