#!/usr/bin/env bash
set -euxo pipefail

if [[ "$1" == "" ]]; then
    echo "This script requires one argument specifying which Python version to use (e.g. 2.7)"
    exit 1
fi

BUILDKITE_DIR="$(dirname "${BASH_SOURCE[0]}")"
source ${BUILDKITE_DIR}/setup_python.sh $1

pip install -r tests/requirements.txt

# Run the unit tests
pytest tests/unit/
