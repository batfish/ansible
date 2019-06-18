#!/usr/bin/env bash
set -euo pipefail

# Setup conda so we can avoid permission issues setting up Python as non-root user
curl -o conda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash conda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
conda create -y -n conda_env python=3.7
source activate conda_env

# Setup Ansible, and our Ansible role
pip install ansible
ansible-galaxy install --force batfish.base
