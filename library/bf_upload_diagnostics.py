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
module: bf_upload_diagnostics
short_description: Upload anonymized diagnostic information about a Batfish snapshot
version_added: "2.7"
description:
    - Fetches, anonymizes, and uploads diagnostic information about a Batfish snapshot.  This runs a series of diagnostic questions on the specified snapshot, which are then anonymized with Netconan (U(https://github.com/intentionet/netconan)), and optionally uploaded to the Batfish developers.
options:
    network:
        description:
            - Name of the network to collect diagnostic information from.
        required: false
        default: Value in the C(bf_network) fact.
        type: str
    snapshot:
        description:
            - Name of the snapshot to collect diagnostic information about.
        required: false
        default: Value in the C(bf_snapshot) fact.
        type: str
    contact_info:
        description:
            - Contact information associated with this upload.
        required: false
        type: str
    dry_run:
        default: true
        description:
            - Whether or not to skip upload. If C(true), upload is skipped and the anonymized files will be stored locally for review. If C(false), anonymized files will be uploaded to the Batfish developers.
        required: false
        type: bool
    netconan_config:
        default: Anonymize passwords and IP addresses.
        description:
            - Path to Netconan (U(https://github.com/intentionet/netconan)) configuration file, containing settings used for information anonymization.
        required: false
        type: bool
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
# Generate diagnostic information about the specified snapshot and save locally (do not upload)
- bf_upload_diagnostics
    network: datacenter_sea
    snapshot: 2019-01-01
    dry_run: true
    contact_info: my.email@example.com
# Generate diagnostic information about the specified snapshot and upload to the Batfish developers
- bf_upload_diagnostics
    network: datacenter_sea
    snapshot: 2019-01-01
    dry_run: false
    contact_info: my.email@example.com
'''

RETURN = '''
summary:
    description: Summary of action(s) performed.
    type: str
    returned: always
'''

import os

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
        contact_info=dict(type='str', required=False),
        dry_run=dict(type='bool', required=False, default=True),
        netconan_config=dict(type='str', required=False),
        session=dict(type='dict', required=True),
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
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

    network = module.params['network']
    snapshot = module.params['snapshot']
    contact_info = module.params.get('contact_info')
    netconan_config = module.params.get('netconan_config')
    dry_run = module.params['dry_run']
    session_params = module.params.get('session', {})

    try:
        session = create_session(**session_params)
    except Exception as e:
        message = 'Failed to establish session with Batfish service: {}'.format(e)
        module.fail_json(msg=message, **result)
        return

    try:
        session.set_network(network)
        session.set_snapshot(snapshot)
    except Exception as e:
        message = 'Failed to find snapshot {} in network {}: {}'.format(snapshot, network, e)
        module.fail_json(msg=message, **result)

    if netconan_config:
        if not os.path.isfile(netconan_config):
            message = 'Specified netconan_config is invalid. Must specify a file.'
            module.fail_json(msg=message, **result)

    try:
        upload_result = session.upload_diagnostics(dry_run=dry_run,
                                                   netconan_config=netconan_config,
                                                   contact_info=contact_info)
        if dry_run:
            summary = 'Diagnostics for snapshot {} on network {} written to temporary directory: {}'.format(
                snapshot, network, upload_result)
        else:
            summary = 'Diagnostics for snapshot {} on network {} uploaded successfully.'.format(
                snapshot, network)
    except Exception as e:
        message = 'Failed to upload diagnostics: {}'.format(e)
        module.fail_json(msg=message, **result)
        return

    result['summary'] = summary
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
