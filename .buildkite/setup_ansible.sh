#!/usr/bin/env bash
# Setup Ansible and our Batfish Ansible role
set -euo pipefail

pip install ansible

ansible-galaxy install --force git+https://github.com/batfish/ansible.git,${BUILDKITE_BRANCH}
