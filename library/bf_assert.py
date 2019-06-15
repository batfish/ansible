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
            - List of assertions to make about the snapshot.
            - See U(assertions.rst) for documentation of supported assertions.
        required: true
        type: list
    network:
        description:
            - Name of the network to make assertions about. 
        default: Value in the C(bf_network) fact.
        required: false
        type: str
    snapshot:
        description:
            - Name of the snapshot to make assertions about. 
        default: Value in the C(bf_snapshot) fact.
        required: false
        type: str
    session:
        description:
            - Batfish session object required to connect to the Batfish service.
        default: Value in C(bf_session) fact.
        required: false
        type: dict
author:
    - Spencer Fraint (`@sfraint <https://github.com/sfraint>`_)
requirements:
    - "pybatfish"
'''

EXAMPLES = '''
# Confirm there are no undefined references or incompatible BGP sessions
- bf_assert:
    assertions:
      - type: assert_no_undefined_references
        name: Confirm we have no undefined references
      - type: assert_no_incompatible_bgp_sessions
        name: Confirm we have no incompatible BGP sessions

# Confirm 10.10.10.10 is reachable by traffic entering Gig0/0 of as1border1
- bf_assert:
    assertions:
      - type: assert_reachable
        name: confirm host is reachable for traffic received on GigEth0/0
        parameters:
          startLocation: '@enter(as1border1[GigabitEthernet0/0])'
          headers:
            dstIps: '10.10.10.10'

# Confirm a filter denies some specific traffic
- bf_assert:
    assertions:
      - type: assert_filter_denies
        name: confirm node1 filter block_access denies TCP traffic on port 22
        parameters:
          filter_name: 'node1["block_access"]'
          headers:
            applications: 'ssh'
'''

RETURN = '''
summary:
    description: Summary of action(s) performed.
    type: str
    returned: always
result:
    description: List of assertion results. There is one entry per assertion, and each entry contains details of the assertion and additional information when the assertion fails.
    type: list
    returned: always
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.bf_util import create_session, set_snapshot
from ansible.module_utils.bf_assertion_util import (
    ASSERT_PASS_MESSAGE, get_assertion_issues, run_assertion
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
    failed = []
    summary = 'Assertion(s) completed successfully'

    try:
        session = create_session(**session_params)
    except Exception as e:
        message = 'Failed to establish session with Batfish service: {}'.format(e)
        module.fail_json(msg=message, **result)
        return

    try:
        set_snapshot(session=session, network=network, snapshot=snapshot)
    except Exception as e:
        message = 'Failed to set snapshot: {}'.format(e)
        module.fail_json(msg=message, **result)
        return

    for assertion in assertions:
        status = 'Pass'
        try:
            assert_result = run_assertion(session, assertion)
            if assert_result != ASSERT_PASS_MESSAGE:
                failed.append(assert_result)
                status = 'Fail'
        except Exception as e:
            assert_result = str(e)
            failed.append(assert_result)
            status = 'Error'

        results.append({
            'name': assertion['name'],
            'type': assertion['type'],
            'status': status,
            'details': assert_result,
        })
    if failed:
        summary = '{} of {} assertions failed'.format(len(failed), len(assertions))

    result['summary'] = summary
    result['result'] = results
    # Indicate failure to Ansible in the case of failed assert(s)
    if failed:
        module.fail_json(msg=summary, **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
