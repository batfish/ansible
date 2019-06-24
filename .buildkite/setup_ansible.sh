#!/usr/bin/env bash
# Setup Ansible and our Batfish Ansible role
set -euo pipefail

pip install ansible

# Install our local Ansible role instead of the one on galaxy
ROLES_DIR=$HOME/.ansible/roles/
mkdir -p ${ROLES_DIR}
ln -s $(pwd) ${ROLES_DIR}batfish.base
