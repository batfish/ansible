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
from pybatfish.client.asserts import (
    assert_filter_denies, assert_filter_permits, assert_flows_fail,
    assert_flows_succeed
)
from pybatfish.exception import BatfishAssertException

# Map assertion-type string to Pybatfish-assertion function
_ASSERT_TYPE_TO_FUNCTION = {
    'assert_reachable': assert_flows_succeed,
    'assert_unreachable': assert_flows_fail,
    'assert_filter_permits': assert_filter_permits,
    'assert_filter_denies': assert_filter_denies,
}

ASSERT_PASS_MESSAGE = 'Assertion passed'

def get_assertion_issues(assertion):
    """Return the reason the assertion dictionary is valid, or return None if it is valid."""
    if not isinstance(assertion, Mapping):
        return "Assertion format is invalid, expected dictionary: {}".format(assertion)

    if 'name' not in assertion:
        return "No name specified for assertion: {}".format(assertion)
    name = assertion['name']

    if 'type' not in assertion:
        return "No type specified for assertion '{}'".format(name)

    params = assertion.get('parameters', {})
    if not isinstance(params, Mapping):
        return "Invalid parameters, expected a dictionary of param name to value for assertion '{}'".format(name)

    type_ = assertion['type']
    if _get_asserts_function_from_type(type_) is None:
        return "Unknown assertion type: {} for assertion '{}'".format(type_, name)
    return None


def _get_asserts_function_from_type(type_):
    """Get the Pybatfish-asserts function for a given Ansible assertion-type string."""
    return _ASSERT_TYPE_TO_FUNCTION.get(type_)


def run_assertion(session, assertion):
    """Run the specified assertion and return the result message."""
    type_ = assertion['type']
    params = deepcopy(assertion.get('parameters', {}))
    params['session'] = session

    assert_ = _get_asserts_function_from_type(type_)
    try:
        assert_(**params)
    except BatfishAssertException as e:
        return str(e)
    return ASSERT_PASS_MESSAGE
