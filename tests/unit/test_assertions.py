from unittest.mock import patch

from pandas import DataFrame
from pybatfish.client.session import Session

from module_utils.bf_assertion_util import get_assertion_issues, run_assertion, \
    ASSERT_PASS_MESSAGE
from tests.unit.test_utils import MockTableAnswer, MockQuestion


def test_get_assertion_issues():
    """Confirm no issues are detected when checking valid assertion dictionary."""
    assert get_assertion_issues({
        'name': 'assertion_name',
        'type': 'assert_all_flows_fail',
        'parameters': {
            'startLocation': 'start',
            'headers': 'headers',
        },
    }) is None, 'No issues from properly formatted assertion'


def test_get_assertion_issues_extra_param():
    """Confirm issue is detected when checking assertion dictionary with extra assertion parameters."""
    issue = get_assertion_issues({
        'name': 'assertion_name',
        'type': 'assert_all_flows_fail',
        'parameters': {
            'startLocation': 'start',
            'headers': 'headers',
            'extraParam': 'extra',
        },
    })
    # Issue message should indicate there is an invalid parameter
    assert 'Invalid parameter' in issue
    # and reference that parameter's name
    assert 'extraParam' in issue


def test_get_assertion_issues_missing_param():
    """Confirm issue is detected when checking assertion dictionary missing some mandatory parameter."""
    issue = get_assertion_issues({
        'name': 'assertion_name',
        'type': 'assert_all_flows_fail',
        'parameters': {
            'startLocation': 'start',
            # missing 'header' param
        },
    })
    # Issue message should indicate there is a missing parameter
    assert 'Missing mandatory parameter' in issue
    # and reference that parameter's name
    assert 'header' in issue


def test_get_assertion_issues_no_name():
    """Confirm issue is detected when checking assertion dictionary missing a name."""
    issue = get_assertion_issues({
        # missing 'name'
        'type': 'assert_all_flows_fail',
        'parameters': {
            'startLocation': 'start',
            'header': 'header',
        },
    })
    # Issue message should indicate name is missing
    assert 'No name specified' in issue


def test_get_assertion_issues_invalid_type():
    """Confirm issue is detected when checking assertion dictionary with an invalid type."""
    issue = get_assertion_issues({
        'name': 'assertion_name',
        'type': 'invalid_assertion_type',
    })
    # Issue message should indicate type is missing
    assert 'Unknown assertion type' in issue


def test_get_assertion_issues_no_type():
    """Confirm issue is detected when checking assertion dictionary missing a type."""
    issue = get_assertion_issues({
        'name': 'assertion_name',
        # missing 'type'
    })
    # Issue message should indicate type is missing
    assert 'No type specified' in issue


def test_run_assertion():
    """Confirm running passing assertion results in a passing message."""
    bf = Session(load_questions=False)
    assertion = {
        'name': 'assert_name',
        'type': 'assert_no_undefined_references',
    }
    with patch.object(bf.q,
                      'undefinedReferences',
                      create=True) as mock_undef:
        mock_undef.return_value = MockQuestion(MockTableAnswer())
    assert run_assertion(bf, assertion) == ASSERT_PASS_MESSAGE


def test_run_assertion_fail():
    """Confirm running failing assertion results in a message indicating failure."""
    bf = Session(load_questions=False)
    assertion = {
        'name': 'assert_name',
        'type': 'assert_no_undefined_references',
    }
    with patch.object(bf.q,
                      'undefinedReferences',
                      create=True) as mock_undef:
        mock_undef.return_value = MockQuestion(
            MockTableAnswer(DataFrame.from_records(
                [{'Undef': 'something'}])))
        result = run_assertion(bf, assertion)
    assert ASSERT_PASS_MESSAGE not in result
    assert 'Found undefined reference(s), when none were expected' in result
