#!/usr/bin/env bash
set -euo pipefail

# Setup conda so we can avoid permission issues setting up Python as non-root user
curl -o conda.sh https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash conda.sh -b -f -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
conda create -y -n conda_env python=3.7
source activate conda_env
# Get around having to build regex since there is no linux wheel
conda install --yes -c conda-forge regex

pip install git+https://github.com/batfish/pybatfish.git
pip install -r requirements.txt
