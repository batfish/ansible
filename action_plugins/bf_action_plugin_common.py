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
from __future__ import (absolute_import, division, print_function)

import os

__metaclass__ = type

from ansible.errors import AnsibleActionFail
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

display = Display()

# Modules that require snapshot (and network) to be explicitly specified
_EXPLICIT_SNAPSHOT_PARAMETER_MODULES = {
    'bf_init_snapshot', 'bf_upload_diagnostics', 'bf_set_snapshot'
}

# Modules that perform assertions on snapshots
_ASSERTION_MODULES = {
    'bf_assert', 'bf_validate_facts'
}


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        # Need to use local connect, since Batfish modules run on localhost only
        if self._play_context.connection != 'local':
            return dict(
                failed=True,
                msg='invalid connection specified, expected connection=local, '
                    'got %s' % self._play_context.connection
            )

        # Use user-specified session or ansible_facts.bf_session in that order
        facts = self._templar.template('{{ansible_facts}}')  # .bf_session
        module_args = self._task.args.copy()

        # Fall-back to using values from Ansible facts for common module parameters
        if 'session' not in module_args:
            session = facts.get('bf_session')
            if session is None:
                raise AnsibleActionFail(
                    'No Batfish session detected. Run the bf_session module to set one up.')
            display.vvv(
                'No session supplied, using session from Ansible facts: %s' % session)
            module_args['session'] = session

        module_name = self._task.action

        # Fall-back to using values from Ansible facts for snapshot/network
        # name for any module that doesn't require these to be explicitly set
        if module_name not in _EXPLICIT_SNAPSHOT_PARAMETER_MODULES:
            if 'snapshot' not in module_args:
                snapshot = facts.get('bf_snapshot')
                if snapshot is None:
                    raise AnsibleActionFail(
                        'No Batfish snapshot detected. Run the bf_init_snapshot '
                        'module to set one up or set the snapshot name via '
                        'bf_set_snapshot module.')
                module_args['snapshot'] = snapshot

            if 'network' not in module_args:
                network = facts.get('bf_network')
                if network is None:
                    raise AnsibleActionFail(
                        'No Batfish network detected. Run the bf_init_snapshot '
                        'module to set one up or set the network name via '
                        'bf_set_snapshot module.')
                module_args['network'] = network

        if module_name in _ASSERTION_MODULES:
            if 'bf_policy_name' not in os.environ:
                os.environ['bf_policy_name'] = self._templar.template(
                    '{{ansible_play_name}}')
            if 'bf_policy_id' not in os.environ:
                os.environ['bf_policy_id'] = self._play_context._uuid
            if 'bf_test_name' not in os.environ:
                os.environ['bf_test_name'] = self._task.name

        result = self._execute_module(module_name=module_name,
                                      module_args=module_args,
                                      task_vars=task_vars,
                                      wrap_async=self._task.async_val)
        return result
