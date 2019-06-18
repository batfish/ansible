#!/usr/bin/env bash
# Setup Ansible and our Batfish Ansible role
set -euxo pipefail

pip install ansible
ansible-galaxy install --force batfish.base
