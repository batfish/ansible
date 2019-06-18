#!/usr/bin/env bash
set -euo pipefail

# Run everything in a virtual environment
pip install virtualenv
python -m virtualenv venv
source venv/bin/activate

# Setup Ansible, and our Ansible role
pip install ansible
ansible-galaxy install --force batfish.base
