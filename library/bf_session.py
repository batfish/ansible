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
module: bf_session
short_description: Builds a Batfish session for use with other Batfish Ansible modules
version_added: "2.7"
description:
    - "Builds a Batfish session for use with other Batfish Ansible modules and populates C(bf_session) fact."
options:
    host:
        description:
            - Host (resolvable name or IP address) running the Batfish service.
        required: true
    name:
        description:
            - Name of the session.
        required: false
    parameters:
        description:
            - Dictionary with additional parameters used to configure the session.  See U(https://pybatfish.readthedocs.io/en/latest/api.html#session-parameters) for more details.
        required: false
author:
    - Spencer Fraint (`@sfraint <https://github.com/sfraint>`_)
requirements:
    - "pybatfish"
'''

EXAMPLES = '''
# Establish session with Batfish service running on localhost
- bf_session:
    host: localhost
    name: my_session
# Establish SSL session with Batfish service running at 10.10.10.10
- bf_session:
    host: 10.10.10.10
    name: my_session
    parameters:
      ssl: true
'''

RETURN = '''
# TODO
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.bf_util import create_session

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
        host=dict(type='str', required=True),
        name=dict(type='str', required=False, default='default'),
        parameters=dict(type='dict', required=False),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        session='',
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

    host = module.params['host']
    name = module.params['name']
    parameters = module.params['parameters']

    if parameters is None:
        parameters = {}
    parameters['host'] = host

    # Not strictly necessary, but useful to confirm the session can be established
    create_session(**parameters)

    # Overall status of command execution
    result['summary'] = "Session established to '{}' ({})".format(host, name)
    result['session'] = parameters
    result['changed'] = True
    result['ansible_facts']['bf_session'] = parameters
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
