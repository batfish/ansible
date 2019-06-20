#!/usr/bin/env bash
set -euxo pipefail

BUILDKITE_DIR="$(dirname "${BASH_SOURCE[0]}")"
source ${BUILDKITE_DIR}/setup_python.sh

pip install -r tests/requirements.txt

# Run the unit tests
pytest tests/unit/
