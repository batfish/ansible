#!/usr/bin/python
#   Copyright 2018 The Batfish Open Source Project
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
module: bf_extract_facts
short_description: Extracts facts from the current Batfish snapshot
version_added: "2.7"
description:
    - "Extracts facts from the current Batfish snapshot"
options:
    nodes:
        description:
            - Nodes to extract facts for.
        required: false
    output_directory:
        description:
            - Optional directory to save facts to.
        required: false
    session:
        description:
            - Batfish session required to connect to the Batfish service.
        required: true
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

import json
import os
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.bf_util import (create_session, get_facts,
                                          write_facts)

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
        nodes=dict(type='str', required=False, default='.*'),
        network=dict(type='str', required=True),
        snapshot=dict(type='str', required=True),
        output_directory=dict(type='str', required=False),
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

    output_directory = module.params['output_directory']
    nodes = module.params['nodes']
    session_params = module.params.get('session', {})
    network = module.params.get('network')
    snapshot = module.params.get('snapshot')

    session = create_session(network=network, snapshot=snapshot, **session_params)

    facts = get_facts(session, nodes_specifier=nodes)
    summary = "Got facts for nodes: '{}'".format(nodes)

    if output_directory:
        write_facts(output_directory, facts)
        summary += ', wrote facts to directory: {}'.format(output_directory)

    # Overall status of command execution
    result['summary'] = summary
    result['result'] = facts
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
