#!/usr/bin/env bash
set -euxo pipefail

BUILDKITE_DIR="$(dirname "${BASH_SOURCE[0]}")"
source ${BUILDKITE_DIR}/setup_python.sh
source ${BUILDKITE_DIR}/setup_ansible.sh

pushd tutorials

# Run docker setup
#ansible-playbook -i inventory playbooks/batfish_docker_setup.yml
# Run setup playbook
ansible-playbook -i inventory playbooks/batfish_setup.yml

# Run the tutorials
ansible-playbook -i inventory playbooks/tutorial1_extract_facts.yml
ansible-playbook -i inventory playbooks/tutorial2_validate_facts.yml
ansible-playbook -i inventory playbooks/tutorial3_validate_forwarding.yml
ansible-playbook -i inventory playbooks/tutorial4_validate_acls.yml
ansible-playbook -i inventory playbooks/tutorial5_validate_bgp_sessions.yml
