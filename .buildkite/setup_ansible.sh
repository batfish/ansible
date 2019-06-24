#!/usr/bin/env bash
# Setup Ansible and our Batfish Ansible role
set -euo pipefail

pip install ansible

# Install our Ansible role from the current branch source
ROLES_DIR=$HOME/.ansible/roles/
mkdir -p ${ROLES_DIR}
ln -s $(pwd) ${ROLES_DIR}batfish.base
