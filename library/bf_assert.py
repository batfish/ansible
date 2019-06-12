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
module: bf_assert
short_description: Makes assertions about a Batfish snapshot
version_added: "2.7"
description:
    - "Makes assertions about the contents and/or behavior of a Batfish snapshot."
options:
    assertions:
        description:
            - List of assertions to make on the snapshot.
        required: true
    network:
        description:
            - Name of the network to make assertions about. This defaults to the value in the C(bf_network) fact.  
        required: false
    snapshot:
        description:
            - Name of the snapshot to make assertions about. This defaults to the value in the C(bf_snapshot) fact.  
        required: false
    session:
        description:
            - Batfish session parameters required to connect to the Batfish service. This defaults to the value in C(bf_session) fact.
        required: false
author:
    - Spencer Fraint (`@sfraint <https://github.com/sfraint>`_)
requirements:
    - "pybatfish"
'''

EXAMPLES = '''
# Confirm 10.10.10.10 is unreachable by traffic entering Gig0/0 of as1border1
- bf_assert:
    assertions:
      - type: assert_unreachable
        name: confirm host is unreachable from inlet
        parameters:
          startLocation: "@enter(as1border1[GigabitEthernet0/0])"
          headers:
            dstIps: 10.10.10.10
'''

RETURN = '''
summary:
    description: Summary of action(s) performed.
    type: str
result:
    description: List of high-level assertion results (name and status).
    type: list
result_verbose:
    description: List of verbose assertion results, containing more details about why assertions failed.
    type: list
'''

from ansible.errors import AnsibleActionFail, AnsibleError
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.bf_util import create_session, set_snapshot
from ansible.module_utils.bf_assertion_util import (get_assertion_issues,
                                                    run_assertion)

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
        assertions=dict(type='list', required=False, default='.*'),
        network=dict(type='str', required=True),
        snapshot=dict(type='str', required=True),
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
        result_verbose='',
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

    assertions = module.params.get('assertions')
    session_params = module.params.get('session')
    network = module.params.get('network')
    snapshot = module.params.get('snapshot')

    issues = [i for i in [get_assertion_issues(a) for a in assertions] if i]
    if any(issues):
        message = (
            '{} of {} assertions are malformed'.format(len(issues), len(assertions))
            + ', no assertions run'
        )
        result['result'] = issues
        module.fail_json(msg=message, **result)

    if module.check_mode:
        module.exit_json(**result)

    results = []
    results_verbose = []
    failed = []
    summary = 'Assertion(s) completed successfully'

    session = create_session(**session_params)
    set_snapshot(session=session, network=network, snapshot=snapshot)
    for assertion in assertions:
        status = 'Pass'
        assert_result = run_assertion(session, assertion)

        if assert_result:
            failed.append(assert_result)
            status = 'Fail'
        else:
            assert_result = 'Assertion passed'

        results.append({
            'name': assertion['name'],
            'status': status,
        })
        results_verbose.append({
            'name': assertion['name'],
            'type': assertion['type'],
            'status': status,
            'details': assert_result,
        })
    if failed:
        summary = '{} of {} assertions failed'.format(len(failed), len(assertions))
        # Add warning that shows up in Ansible in the case of failed assert(s)
        result['warnings'] = [summary]

    # Overall status of command execution
    result['summary'] = summary
    result['result'] = results
    result['result_verbose'] = results_verbose
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
