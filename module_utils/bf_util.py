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

from pybatfish.client._diagnostics import (
    check_if_all_passed, check_if_any_failed, get_snapshot_parse_status
)
from pybatfish.client.session import Session

_UPLOAD_DIAGNOSTICS_DOC_URL = 'https://github.com/batfish/ansible/blob/master/docs/bf_upload_diagnostics.rst'

NODE_SPECIFIER_INSTRUCTIONS_URL = 'https://github.com/batfish/batfish/blob/master/questions/Parameters.md#node-specifier'


def create_session(session_type='bf', **params):
    """Create session with the supplied params."""
    return Session.get(type_=session_type, **params)


def set_snapshot(session, network, snapshot):
    """Set the network and snapshot for the specified session."""
    session.set_network(network)
    session.set_snapshot(snapshot)


def get_snapshot_init_warning(session):
    """Return warning message if the snapshot initialization had issues (parse warnings, errors)."""
    statuses = get_snapshot_parse_status(session)
    if check_if_any_failed(statuses):
        return 'Your snapshot was initialized but Batfish failed to parse one or more input files. You can proceed but some analysis may be incorrect. You can help the Batfish developers improve support for your network by running the bf_upload_diagnostics module: {}'.format(
            _UPLOAD_DIAGNOSTICS_DOC_URL)
    if not check_if_all_passed(statuses):
        return 'Your snapshot was successfully initialized but Batfish failed to fully recognized some lines in one or more input files. Some unrecognized configuration lines are not uncommon for new networks, and it is often fine to proceed with further analysis.  You can help the Batfish developers improve support for your network by running the bf_upload_diagnostics module: {}'.format(
            _UPLOAD_DIAGNOSTICS_DOC_URL)
    return None


def get_node_count(facts):
    """Return the number of nodes in the supplied facts."""
    nodes, version = _unencapsulate_facts(facts)
    return len(nodes)


def _unencapsulate_facts(facts, check_version=False):
    """Extract node facts and version from final fact format."""
    assert 'nodes' in facts, 'No nodes present in parsed facts file(s)'
    return facts['nodes'], facts.get('version')
