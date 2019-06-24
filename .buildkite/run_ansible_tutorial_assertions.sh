#!/usr/bin/env bash
set -euxo pipefail

if [[ "$1" == "" ]]; then
    echo "This script requires one argument specifying which Python version to use (e.g. 2.7)"
    exit 1
fi

BUILDKITE_DIR="$(dirname "${BASH_SOURCE[0]}")"
source ${BUILDKITE_DIR}/setup_python.sh $1
source ${BUILDKITE_DIR}/setup_ansible.sh

pushd tutorials
# Run setup playbook
ansible-playbook -i inventory --extra-vars "batch_mode=True" playbooks/batfish_setup.yml
popd

# Run the tutorial assertions playbook, validating the output of the tutorials
ansible-playbook -i inventory tests/e2e/test_tutorials.yml
