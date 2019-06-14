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
        type: str
    name:
        default: default
        description:
            - Name of the session.
        required: false
        type: str
    parameters:
        default: C(empty)
        description:
            - Dictionary with additional parameters used to configure the session. Use C({ssl: true}) to use SSL.
        required: false
        type: dict
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
summary:
    description: Summary of action(s) performed.
    type: str
    returned: always
session:
    description: Details about the created session.
    type: complex
    contains:
        host:
            description: Host where service is hosted
            type: str
            returned: always
        parameters:
            description: Additional parameters to connect to the service
            type: dict
            returned: if supplied by user
    returned: always
'''

import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.bf_util import create_session

try:
    from pybatfish.client.session import Session
except Exception as e:
    pybatfish_found = False
else:
    pybatfish_found = True

# Constants for session creation retry
_MAX_RETRY_TIME = 10
_RETRY_DELAY = 3

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
    try:
        # Allow a few retries in case the service isn't ready yet
        retry_time = 0
        while True:
            try:
                create_session(**parameters)
                break
            except Exception as session_e:
                if retry_time < _MAX_RETRY_TIME:
                    time.sleep(_RETRY_DELAY)
                    retry_time += _RETRY_DELAY
                else:
                    raise session_e
    except Exception as e:
        message = 'Failed to establish session with Batfish service: {}'.format(e)
        module.fail_json(msg=message, **result)

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
