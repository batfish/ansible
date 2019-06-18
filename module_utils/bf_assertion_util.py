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
from inspect import signature
from inspect import _empty as inspect_empty
from pybatfish.client.asserts import (
    assert_filter_has_no_unreachable_lines, assert_filter_denies, assert_filter_permits,
    assert_flows_fail, assert_flows_succeed,
    assert_no_incompatible_bgp_sessions,
    assert_no_undefined_references,
    assert_no_unestablished_bgp_sessions
)
from pybatfish.exception import BatfishAssertException

ASSERTIONS = '''
assert_all_flows_fail:
    short_description: Assert that all packets with specified start locations and headers fail
    description:
        - "This is an all-to-all test that analyzes all (start location, header) combinations"
        - "If any flow (start location, header) can reach its destination, this assertion will return false."
        - "If no flow (start location, header) can reach its destination, this assertion will return true."
        - "This assertion is used to evaluate the security of select destinations in the network."
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
        - "This is an all-to-all test that analyzes all (start location, header) combinations"
        - "If any flow (start location, header) cannot reach its destination, this assertion will return false."
        - "If all flows (start location, header) can reach its destination, this assertion will return true."
        - "This assertion is used to evaluate the accessibility of select destinations in the network."
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
        - "This test will fail if any line in any of the specified filter(s) is unreachable."
    options:
        filters:
            description:
                - Filter specifier. See U(https://github.com/batfish/batfish/blob/master/questions/Parameters.md#filter-specifier) for filter specification.
            required: true
            type: dict

assert_filter_denies:
    short_description: Assert that the specified filters (e.g., ACLs) deny specified headers
    description:
        - "This test will fail if any packet in the specified header space is permitted by any of the specified filter(s)."
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
        - "This test will fail if any packet in the specified header space is denied by any of the specified filter(s)."
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

assert_no_unestablished_bgp_sessions:
    short_description: Assert that all compatibly-configured BGP sessions are established
    description:
        - "This test fails if there are any BGP session in the snapshot that are compatibly configured but will not be established (e.g., due to ACLs)."
        - "This test takes no parameters."

assert_no_undefined_references:
    short_description: Assert that there are no undefined references
    description:
        - "This test will fail if any device configuration refers to a structure (e.g., ACL, prefix-list, routemap) that is not defined in the configuration."
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
    'assert_no_unestablished_bgp_sessions': assert_no_unestablished_bgp_sessions,
    'assert_no_undefined_references': assert_no_undefined_references,
}

ASSERT_PASS_MESSAGE = 'Assertion passed'

UNSUPPORTED_ASSERTION_PARAMETERS = {"session", "snapshot", "soft", "df_format"}


def get_assertion_issues(assertion):
    """Return the reason the assertion dictionary is valid, or return None if it is valid."""
    if not isinstance(assertion, Mapping):
        return "Assertion format is invalid, expected dictionary: {}".format(assertion)

    if 'name' not in assertion:
        return "No name specified for assertion: {}".format(assertion)
    name = assertion['name']

    valid_assert_types = ', '.join(_ASSERT_TYPE_TO_FUNCTION.keys())
    if 'type' not in assertion:
        return "No type specified for assertion '{}'. Valid assert types are: {}".format(name, valid_assert_types)

    params = assertion.get('parameters', {})
    if not isinstance(params, Mapping):
        return "Invalid parameters, expected a dictionary of param name to value for assertion '{}'".format(name)

    type_ = assertion['type']
    assert_func = _get_asserts_function_from_type(type_)
    if not assert_func:
        return "Unknown assertion type '{}' for assertion '{}'. Valid assert types are: {}".format(type_, name,
                                                                                                  valid_assert_types)

    parameter_issues = _get_parameter_issues(type_, assert_func, params)
    if parameter_issues:
        return parameter_issues

    return None


def _get_asserts_function_from_type(type_):
    """Get the Pybatfish-asserts function for a given Ansible assertion-type string."""
    return _ASSERT_TYPE_TO_FUNCTION.get(type_)


def _get_parameter_issues(assert_type, assert_func, params):
    """Checks if the parameters supplied to an assertion are valid"""

    assert_func_sig = signature(assert_func)

    valid_params = set(assert_func_sig.parameters) - UNSUPPORTED_ASSERTION_PARAMETERS

    extra_params = params.keys() - valid_params
    if len(extra_params) > 0:
        return "Invalid parameter(s) for {}: {} (valid parameters are {})".format(assert_type, extra_params,
                                                                                  valid_params)

    mandatory_params = {param for param in valid_params if (assert_func_sig.parameters[param].default == inspect_empty)}

    missing_params = mandatory_params - params.keys()
    if len(missing_params) > 0:
        return "Missing mandatory parameter(s) for {}: {}".format(assert_type, missing_params)

    return None


def run_assertion(session, assertion):
    """Run the specified assertion and return the result message."""
    type_ = assertion['type']
    params = deepcopy(assertion.get('parameters', {}))
    params['session'] = session
    params['df_format'] = "records"

    assert_ = _get_asserts_function_from_type(type_)
    try:
        assert_(**params)
    except BatfishAssertException as e:
        return str(e)
    return ASSERT_PASS_MESSAGE
