#!/usr/bin/env bash
# Setup Ansible and our Batfish Ansible role
set -euo pipefail

pip install ansible
# Install our local Ansible role instead of the one on galaxy
ln -s $(pwd) $HOME/.ansible/roles/batfish.base/
