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
    assert_filter_has_no_unreachable_lines, assert_filter_denies, assert_filter_permits,
    assert_flows_fail, assert_flows_succeed,
    assert_no_incompatible_bgp_sessions,
    assert_no_undefined_references
)
from pybatfish.exception import BatfishAssertException

ASSERTIONS = '''
assert_all_flows_fail:
    short_description: Assert that all packets with specified start locations and headers fail
    description:
        - "Success means reaching the destination or exiting the network. Other outcomes such as being denied by an ACL or being dropped due to missing routing information are deemed as a failure."
        - "This is an all-to-all test. It will fail if any (start location, header) combination succeed."
    options:
        start:
            description:
                - Start location specifier. See U(https://github.com/batfish/batfish/blob/master/questions/Parameters.md#location-specifier) for location specification.
            required: true
            type: str
        headers:
            description:
                - Constraints on packet headers. See U(https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints) for keys in this dictionary.
            required: true
            type: dict

assert_all_flows_succeed:
    short_description: Assert that all packets with specified start locations and headers are successful
    description:
        - "Success means reaching the destination or exiting the network. Other outcomes such as being denied by an ACL or being dropped due to missing routing information are deemed as a failure."
        - "This is an all-to-all test. It will fail if any (start location, header) combination fails."
    options:
        start:
            description:
                - Start location specifier. See U(https://github.com/batfish/batfish/blob/master/questions/Parameters.md#location-specifier) for location specification.
            required: true
            type: str
        headers:
            description:
                - Constraints on packet headers. See U(https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints) for keys in this dictionary.
            required: true
            type: dict

assert_filter_has_no_unreachable_lines:
    short_description: Assert that the filters (e.g., ACLs) have no unreachable lines
    description:
        - "A filter line is considered unreachable if it will never match a packet, e.g., because its match condition is empty or covered completely by those of prior lines."
        - "This test will fail if any line in any filter is unreachable."
    options:
        filters:
            description:
                - Filter specifier. See U(https://github.com/batfish/batfish/blob/master/questions/Parameters.md#filter-specifier) for filter specification.
            required: true
            type: dict

assert_filter_denies:
    short_description: Assert that the specified filters (e.g., ACLs) deny specified headers
    description:
        - "This test will fail if any packet in the specified header space is permitted by any filter."
    options:
        filters:
            description:
                - Filter specifier. See U(https://github.com/batfish/batfish/blob/master/questions/Parameters.md#filter-specifier) for filter specification.
            required: true
            type: dict
        headers:
            description:
                - Constraints on packet headers. See U(https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints) for keys in this dictionary.
            required: true
            type: dict

assert_filter_permits:
    short_description: Assert that the specified filters  (e.g., ACLs) permit specified headers
    description:
        - "This test will fail if any packet in the specified header space is denied by any filter."
    options:
        filters:
            description:
                - Filter specifier. See U(https://github.com/batfish/batfish/blob/master/questions/Parameters.md#filter-specifier) for filter specification.
            required: true
            type: dict
        headers:
            description:
                - Constraints on packet headers. See U(https://pybatfish.readthedocs.io/en/latest/datamodel.html#pybatfish.datamodel.flow.HeaderConstraints) for keys in this dictionary.
            required: true
            type: dict

assert_no_incompatible_bgp_sessions:
    short_description: Assert that all BGP sessions are compatibly configured
    description:
        - "This test finds all pairs of BGP session endpoints in the snapshot and will fail if the configuration of any pair is incompatible."
        - "This test takes no parameters."

assert_no_undefined_references:
    short_description: Assert that there are no undefined references
    description:
        - "This test will fail if any device configuration refers to a structured (e.g., ACL or routemap) that is not defined in the configuration."
        - "This test takes no parameters."
'''

# Map assertion-type string to Pybatfish-assertion function
_ASSERT_TYPE_TO_FUNCTION = {
    'assert_all_flows_fail': assert_flows_fail,
    'assert_all_flows_succeed': assert_flows_succeed,
    'assert_filter_has_no_unreachable_lines': assert_filter_has_no_unreachable_lines,
    'assert_filter_denies': assert_filter_denies,
    'assert_filter_permits': assert_filter_permits,
    'assert_no_incompatible_bgp_sessions': assert_no_incompatible_bgp_sessions,
    'assert_no_undefined_references': assert_no_undefined_references,
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
