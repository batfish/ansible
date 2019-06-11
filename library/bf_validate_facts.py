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
module: bf_validate_facts
short_description: Validates facts for the current Batfish snapshot against the facts in the supplied directory 
version_added: "2.7"
description:
    - "Validates facts for the current Batfish snapshot against the facts in the supplied directory"
options:
    nodes:
        description:
            - Nodes to extract facts for.
        required: false
    input_directory:
        description:
            - Directory to pull known good facts from.
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
from ansible.module_utils.bf_util import (assert_dict_subset, create_session,
                                          get_facts, load_facts)

try:
    from pybatfish.client.session import Session
    # from pybatfish.client.asserts import assert_dict_subset
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
        input_directory=dict(type='str', required=True),
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

    nodes_spec = module.params['nodes']
    input_directory = module.params['input_directory']
    session_params = module.params.get('session', {})
    network = module.params.get('network')
    snapshot = module.params.get('snapshot')

    session = create_session(network=network, snapshot=snapshot, **session_params)

    facts = get_facts(session, nodes_specifier=nodes_spec)
    expected_facts = load_facts(input_directory)['nodes']

    failures = {}
    nodes_facts = facts['nodes']
    # result['result'] = {'expected': expected_facts}
    # result['result']['nodes_facts'] = nodes_facts
    for node in nodes_facts:
        #try:
        if node in expected_facts:
            #result['result'][node] = {
            #    'expected': expected_facts[node],
            #    'actual': nodes_facts[node],
            #}
            res = assert_dict_subset(nodes_facts[node], expected_facts[node])
            if res:
                failures[node] = res
    # except Exception as e:
    #    failures[node] = str(e)

    summary = 'Actual facts match expected facts'
    if failures:
        summary = ('Validation failed for the following nodes: {}. See task ' +
                   'output for more details.').format(list(failures.keys()))

    # Overall status of command execution
    result['summary'] = summary
    # Detailed results
    result['result'] = failures
    # Also warn the user in the case of failed assert(s)
    if failures:
        result['warnings'] = [summary]

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
