#!/usr/bin/env bash
# Setup python for running Batfish Ansible modules and tutorials
set -euo pipefail

# Setup conda so we can avoid permission issues setting up Python as non-root user
curl -o conda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash conda.sh -b -f -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
conda create -y -n conda_env python=3.7
source activate conda_env
# Get around having to build regex since there is no linux wheel in PyPI
conda install --yes -c conda-forge regex

# Setup a virtual environment as well, so the setup playbook does not complain
pip install virtualenv
python -m virtualenv venv
source venv/bin/activate
