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
module: bf_extract_facts
short_description: Extracts facts for a Batfish snapshot
version_added: "2.7"
description:
    - "Extracts and returns facts for a Batfish snapshot and saves them (one YAML file node) to the output directory if specified."
options:
    nodes:
        description:
            - Nodes to extract facts for. See U(https://github.com/batfish/batfish/blob/master/questions/Parameters.md#node-specifier) for more details on node specifiers.
        required: false
        type: str
        default: All nodes
    network:
        description:
            - Name of the network to extract facts for. 
        default: Value in the C(bf_network) fact.
        required: false
        type: str
    snapshot:
        description:
            - Name of the snapshot to extract facts for. 
        default: Value in the C(bf_snapshot) fact.
        required: false
        type: str
    output_directory:
        default: None
        description:
            - Directory to save facts to.
        required: false
        type: str
    session:
        description:
            - Batfish session object required to connect to the Batfish service. 
        default: Value in the C(bf_session) fact.
        required: false
        type: dict
author:
    - Spencer Fraint (`@sfraint <https://github.com/sfraint>`_)
requirements:
    - "pybatfish"
'''

EXAMPLES = '''
# Extract facts and save to an output directory
- bf_extract_facts:
    output_directory: output/facts/
# Extract facts for nodes whose names contain as1border or host
- bf_extract_facts:
    nodes: /as1border|host/
'''

RETURN = '''
summary:
    description: Summary of action(s) performed.
    type: str
    returned: always
result:
    description: Dictionary of extracted facts.
    type: complex
    contains:
        nodes:
            description: Dictionary of node-name to node-facts for each node.
            type: complex
            returned: always
        version:
            description: Fact-format version of the returned facts.
            type: str
            returned: always
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.bf_util import (create_session, get_node_count,
                                          set_snapshot,
                                          NODE_SPECIFIER_INSTRUCTIONS_URL)

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

    try:
        session = create_session(**session_params)
    except Exception as e:
        message = 'Failed to establish session with Batfish service: {}'.format(
            e)
        module.fail_json(msg=message, **result)
        return

    try:
        set_snapshot(session=session, network=network, snapshot=snapshot)
    except Exception as e:
        message = 'Failed to set snapshot: {}'.format(e)
        module.fail_json(msg=message, **result)
        return

    try:
        facts = session.extract_facts(nodes=nodes,
                                      output_directory=output_directory)
        if not get_node_count(facts):
            result['warnings'] = [
                'No nodes found matching node specifier "{}". See here for details on how to use node specifiers: {}'.format(
                    nodes, NODE_SPECIFIER_INSTRUCTIONS_URL)]
    except Exception as e:
        message = 'Failed to extract facts: {}'.format(e)
        module.fail_json(msg=message, **result)
        return

    summary = "Got facts for nodes: '{}'".format(nodes)
    if output_directory:
        summary += ', wrote facts to directory: {}'.format(output_directory)

    # Overall status of command execution
    result['summary'] = summary
    result['result'] = facts
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
