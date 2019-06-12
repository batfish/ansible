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

from copy import deepcopy
from collections import Mapping
from pybatfish.client.asserts import (assert_flows_fail, assert_flows_succeed)
from pybatfish.exception import BatfishAssertException

def check_assertion_issues(assertion):
    """Confirm the assertion is valid."""
    if 'name' not in assertion:
        return "No name specified for the assertion. {}".format(assertion)
    if 'type' not in assertion:
        return "No type specified for the assertion. {}".format(assertion)
    params = assertion.get('parameters', {})
    if not isinstance(params, Mapping):
        return "Invalid parameters, expected a dictionary of param name to value. {}".format(assertion)
    return False


def _get_asserts_function_from_type(type_):
    """Get the Pybatfish asserts function from the Ansible assertion type."""
    if type_ == 'assert_reachable':
        return assert_flows_succeed
    elif type_ == 'assert_unreachable':
        return assert_flows_fail
    elif type_ == 'assert_filter_permits':
        pass
    elif type_ == 'assert_filter_denies':
        pass
    elif type_ == 'assert_no_undefined_references':
        pass
    elif type_ == 'assert_no_incompatible_bgp_sessions':
        pass


def run_assertion(session, assertion):
    """Run the specified assertion."""
    name = assertion['name']
    type_ = assertion['type']
    params = deepcopy(assertion.get('parameters', {}))
    params['session'] = session

    assert_ = _get_asserts_function_from_type(type_)
    try:
        assert_(**params)
    except BatfishAssertException as e:
        return str(e)
    return
