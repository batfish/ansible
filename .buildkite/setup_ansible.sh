#!/usr/bin/env bash
set -euxo pipefail

# Setup Ansible, and our Ansible role
pip install ansible
ansible-galaxy install --force batfish.base
