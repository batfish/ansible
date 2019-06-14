#!/usr/bin/python
#   Copyright 2019 The Batfish Open Source Project
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

# Note: these docs take into account the fact that the plugin handles supplying default values for some params
DOCUMENTATION = '''
---
module: bf_init_snapshot
short_description: Initializes a Batfish snapshot with provided snapshot data
version_added: "2.7"
description:
    - "Initializes a Batfish snapshot with provided snapshot data and populates C(bf_network) and C(bf_snapshot) facts."
options:
    network:
        description:
            - Name of the network in which to initialize the snapshot.
        required: true
        type: str
    snapshot:
        description:
            - Name of the snapshot to initialize.
        required: true
        type: str
    snapshot_data:
        description:
            - Path to snapshot data directory or zip. See U(https://github.com/batfish/batfish/wiki/Packaging-snapshots-for-analysis) for more details on packaging your snapshot for analysis.
        required: true
        type: str
    overwrite:
        default: false
        description:
            - Boolean indicating if the snapshot name already exists in the specified network.
        required: false
        type: bool
    session:
        default: value in the C(bf_session) fact
        description:
            - Batfish session parameters required to connect to the Batfish service. This defaults to the value in C(bf_session) fact.
        required: false
        type: dict
author:
    - Spencer Fraint (`@sfraint <https://github.com/sfraint>`_)
requirements:
    - "pybatfish"
'''

EXAMPLES = '''
# Initialize a snapshot with specified snapshot data
- bf_init_snapshot
    network: datacenter_sea
    snapshot: 2019-01-01
    snapshot_data: /path/to/snapshot/data/
# Initialize a snapshot, replacing same named snapshot if it exists
- bf_init_snapshot
    network: network_name
    snapshot: duplicate_snapshot_name
    snapshot_data: /path/to/snapshot/data.zip
    overwrite: true
'''

RETURN = '''
summary:
    description: Summary of action(s) performed.
    type: str
    returned: always
result:
    description: Information about the snapshot created.
    type: complex
    contains:
        snapshot:
            description: Name of the snapshot created.
            type: str
            returned: always
        network:
            description: Name of the network created.
            type: str
            returned: always
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.bf_util import (
    create_session, get_snapshot_init_warning
)

try:
    from pybatfish.client.session import Session
except Exception as e:
    pybatfish_found = False
else:
    pybatfish_found = True

def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        network=dict(type='str', required=True),
        snapshot=dict(type='str', required=True),
        snapshot_data=dict(type='str', required=True),
        overwrite=dict(type='bool', required=False, default=False),
        session=dict(type='dict', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        result='',
        summary='',
        ansible_facts={},
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not pybatfish_found:
        module.fail_json(msg='Python module Pybatfish is required')

    if module.check_mode:
        return result

    network = module.params['network']
    snapshot = module.params['snapshot']
    snapshot_data = module.params['snapshot_data']
    overwrite = module.params['overwrite']
    session_params = module.params.get('session', {})

    try:
        session = create_session(**session_params)
    except Exception as e:
        message = 'Failed to establish session with Batfish service: {}'.format(e)
        module.fail_json(msg=message, **result)
        return

    session.set_network(network)

    try:
        session.init_snapshot(snapshot_data, snapshot, overwrite=overwrite)
    except Exception as e:
        message = 'Failed to initialize snapshot: {}'.format(e)
        module.fail_json(msg=message, **result)

    try:
        warn = get_snapshot_init_warning(session)
        if warn:
            result['warnings'] = [warn]
    except Exception as e:
        result['warnings'] = 'Failed to check snapshot init status: {}'.format(e)

    # Overall status of command execution
    result['summary'] = "Snapshot '{}' created in network '{}'".format(snapshot, network)
    result['result'] = {
        'network': network,
        'snapshot': snapshot,
    }
    result['changed'] = True
    result['ansible_facts']['bf_snapshot'] = snapshot
    result['ansible_facts']['bf_network'] = network

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
