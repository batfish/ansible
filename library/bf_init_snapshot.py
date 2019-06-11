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

DOCUMENTATION = '''
---
module: bf_init_snapshot
short_description: Initializes a Batfish snapshot with provided snapshot data
version_added: "2.7"
description:
    - "Initializes a Batfish snapshot with provided snapshot data"
options:
    network:
        description:
            - Name of the network in which to initialize the snapshot.
        required: true
    snapshot:
        description:
            - Name of the snapshot to initialize.
        required: true
    snapshot_data:
        description:
            - Path to snapshot data directory or zip.
        required: true
    overwrite:
        description:
            - Boolean indicating if the snapshot name already exists in the specified network.
        required: false
    session:
        description:
            - Batfish session required to connect to Batfish service.
        required: false
    debug:
        description:
            - Boolean debug flag (uses local session creation instead of utils)
author:
    - Spencer Fraint (`@sfraint <https://github.com/sfraint>`_)
requirements:
    - "pybatfish"
'''

EXAMPLES = '''
# TODO
'''

RETURN = '''
# TODO
'''

from ansible.module_utils.basic import AnsibleModule

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
        debug=dict(type='bool', required=False, default=False),
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

    if module.params['debug']:
        session = Session(**session_params)
    else:
        from ansible.module_utils.bf_util import create_session
        session = create_session(**session_params)

    session.set_network(network)
    session.init_snapshot(snapshot_data, snapshot, overwrite=overwrite)

    # Overall status of command execution
    result['summary'] = "Snapshot '{}' created in network '{}'".format(snapshot, network)
    result['result'] = {
        'network': network,
        'snapshot': snapshot,
    }
    result['changed'] = True

    # result['ansible_facts']['batfish'] = {'network': network, 'snapshot': snapshot}
    result['ansible_facts']['bf_snapshot'] = snapshot
    result['ansible_facts']['bf_network'] = network

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
