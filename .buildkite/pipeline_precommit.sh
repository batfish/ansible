#!/usr/bin/env bash
set -euo pipefail

BATFISH_DOCKER_CI_BASE_IMAGE="${BATFISH_DOCKER_CI_BASE_IMAGE:-batfish/ci-base:latest}"
DOCKER_PLUGIN_VERSION="${DOCKER_PLUGIN_VERSION:-v3.0.1}"

cat <<EOF
steps:
EOF

###### WAIT a visible marker between pipeline generation and starting.
cat <<EOF
  - wait
EOF

cat <<EOF
  - label: ":ansible: Run Ansible Tutorials"
    command:
      - ".buildkite/run_ansible_tutorial_assertions.sh"
  - label: ":pytest: Run Python unit tests"
    command:
      - ".buildkite/run_python_unit_tests.sh"
    plugins:
      - docker#${DOCKER_PLUGIN_VERSION}:
          image: "${BATFISH_DOCKER_CI_BASE_IMAGE}"
          always-pull: true
EOF
