#!/usr/bin/env bash
set -euo pipefail

BATFISH_DOCKER_CI_BASE_IMAGE="${BATFISH_DOCKER_CI_BASE_IMAGE:-batfish/ci-base:latest}"
DOCKER_PLUGIN_VERSION="${DOCKER_PLUGIN_VERSION:-v3.3.0}"
PYTHON_TEST_VERSIONS=(2.7 3.5 3.6 3.7.3)

cat <<EOF
steps:
EOF

###### WAIT a visible marker between pipeline generation and starting.
cat <<EOF
  - wait
EOF

for version in ${PYTHON_TEST_VERSIONS[@]}; do
cat <<EOF
  - label: ":ansible: Run Ansible Tutorials in Python ${version}"
    command:
      - ".buildkite/run_ansible_tutorial_assertions.sh ${version}"
  - label: ":pytest: Run Python ${version} unit tests"
    command:
      - ".buildkite/run_python_unit_tests.sh ${version}"
    plugins:
      - docker#${DOCKER_PLUGIN_VERSION}:
          image: "${BATFISH_DOCKER_CI_BASE_IMAGE}"
          always-pull: true
EOF
done
