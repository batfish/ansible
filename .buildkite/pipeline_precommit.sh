#!/usr/bin/env bash
set -euo pipefail

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
      - ".buildkite/run_ansible_tutorials.sh"
    agents:
      queue: 'open-source-default'
EOF
