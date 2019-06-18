#!/usr/bin/env bash
set -euo pipefail

# Run everything in a virtual environment
pip3 install virtualenv
python3 -m virtualenv venv
source venv/bin/activate

# Setup Ansible, and our Ansible role
pip3 install ansible
ansible-galaxy install --force batfish.base
