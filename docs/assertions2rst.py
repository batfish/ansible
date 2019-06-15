#!/usr/bin/env python
# (c) 2012, Jan-Piet Mens <jpmens () gmail.com>
#
# This file is part of Ansible
#
# Modified to support stand-alone Galaxy documentation
# Copyright (c) 2014, 2017-2018 Juniper Networks Inc.
#               2014, Rick Sherman
#
# Modified to support stand-alone Galaxy documentation for Batfish
# Copyright (c) 2019 Intentionet, Inc.
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

import ast
import os
import re
import datetime
from jinja2 import Environment, FileSystemLoader
from six import print_

from ansible.module_utils.six import iteritems
from ansible.parsing.plugin_docs import read_docstring
from ansible.parsing.yaml.loader import AnsibleLoader
from ansible.utils.display import Display

display = Display()

try:
    from html import escape as html_escape
except ImportError:
    # Python-3.2 or later
    import cgi


    def html_escape(text, quote=True):
        return cgi.escape(text, quote)


#####################################################################################
# constants and paths

_ITALIC = re.compile(r"I\(([^)]+)\)")
_BOLD = re.compile(r"B\(([^)]+)\)")
_MODULE = re.compile(r"M\(([^)]+)\)")
_URL_W_TEXT = re.compile(r"U\(([^)^|]+)\|([^)]+)\)")
_URL = re.compile(r"U\(([^)^|]+)\)")
_CONST = re.compile(r"C\(([^)]+)\)")
_UNDERSCORE = re.compile(r"_")
DEPRECATED = b" (D)"

ASSERTIONSFILE = "../module_utils/bf_assertion_util.py"
OUTPUTDIR = "./"


#####################################################################################
# this function is modified from the one in plugin_docs.py

def read_docstring(filename, verbose=True, ignore_errors=True):
    """
    Search for assignment of ASSERTIONS variables in the given file.
    Parse DOCUMENTATION from YAML and return the YAML doc or None together with EXAMPLES, as plain text.
    """

    data = {
        'assertions': None,
    }

    string_to_vars = {
        'ASSERTIONS': 'assertions',
    }

    try:
        with open(filename, 'rb') as b_module_data:
            M = ast.parse(b_module_data.read())

        for child in M.body:
            if isinstance(child, ast.Assign):
                for t in child.targets:
                    try:
                        theid = t.id
                    except AttributeError:
                        # skip errors can happen when trying to use the normal code
                        display.warning("Failed to assign id for %s on %s, skipping" % (t, filename))
                        continue

                    if theid in string_to_vars:
                        varkey = string_to_vars[theid]
                        if isinstance(child.value, ast.Dict):
                            data[varkey] = ast.literal_eval(child.value)
                        else:
                            if theid == 'ASSERTIONS':
                                # string should be yaml
                                data[varkey] = AnsibleLoader(child.value.s, file_name=filename).get_single_data()
                            else:
                                # not yaml, should be a simple string
                                data[varkey] = to_text(child.value.s)
                        display.debug('assigned :%s' % varkey)

    except Exception:
        if verbose:
            display.error("unable to parse %s" % filename)
        if not ignore_errors:
            raise

    return data


#####################################################################################

def assertion_to_html(matchobj):
    if matchobj.group(1) is not None:
        assertion_name = matchobj.group(1)
        assertion_href = _UNDERSCORE.sub('-', assertion_name)
        return '<a class="reference internal" href="#' + assertion_href + '"><span class="std std-ref">' + \
                    assertion_name + '</span></a>'
    return ''

def html_ify(text):
    ''' convert symbols like I(this is in italics) to valid HTML '''

    t = html_escape(text)
    t = _ITALIC.sub("<em>" + r"\1" + "</em>", t)
    t = _BOLD.sub("<b>" + r"\1" + "</b>", t)
    t = _MODULE.sub(assertion_to_html, t)
    t = _URL_W_TEXT.sub("<a href='" + r"\2" + "'>" + r"\1" + "</a>", t)
    t = _URL.sub("<a href='" + r"\1" + "'>" + r"\1" + "</a>", t)
    t = _CONST.sub("<code>" + r"\1" + "</code>", t)

    return t


#####################################################################################

def rst_ify(text):
    ''' convert symbols like I(this is in italics) to valid restructured text '''

    try:
        t = _ITALIC.sub(r'*' + r"\1" + r"*", text)
        t = _BOLD.sub(r'**' + r"\1" + r"**", t)
        t = _MODULE.sub(r':ref:`' + r"\1 <\1>" + r"`", t)
        t = _URL_W_TEXT.sub(r'`' + r"\1" + r" <" + r"\2" + r">`_", t)
        t = _URL.sub(r'`' + r"\1" + r" <" + r"\1" + r">`_", t)
        t = _CONST.sub(r'``' + r"\1" + r"``", t)
    except Exception as e:
        raise AnsibleError("Could not process (%s) : %s" % (str(text), str(e)))

    return t


def rst_fmt(text, fmt):
    ''' helper for Jinja2 to do format strings '''

    return fmt % (text)


def rst_xline(width, char="="):
    ''' return a restructured text line of a given length '''

    return char * width


#####################################################################################


def jinja2_environment(template_dir, template_type):
    env = Environment(loader=FileSystemLoader(template_dir),
                      variable_start_string="@{",
                      variable_end_string="}@",
                      trim_blocks=True,
                      )
    env.globals['xline'] = rst_xline

    if template_type == 'assertion':
        env.filters['convert_symbols_to_format'] = rst_ify
        env.filters['html_ify'] = html_ify
        env.filters['fmt'] = rst_fmt
        env.filters['xline'] = rst_xline
        template = env.get_template('assertion.j2')
    else:
        raise Exception("unknown module format type: %s" % template_type)

    return env, template


def process_assertion(assertion_name, assertion_dict, template, out_file):
    print_("Processing  assertion %s" % assertion_name)

    # add name as it does not appear in the dictionary by itself
    assertion_dict['assertion_name'] = assertion_name

    required_fields = ('short_description',)
    for field in required_fields:
        if field not in assertion_dict:
            print_("%s: WARNING: ASSERTION MISSING field '%s'" % (assertion_name, field))

    not_nullable_fields = ('short_description',)
    for field in not_nullable_fields:
        if field in assertion_dict and assertion_dict[field] in (None, ''):
            print_("%s: WARNING: ASSERTION field '%s' is null/empty value=%s" % (
                assertion_name, field, assertion_dict[field]))

    #
    # The present template gets everything from doc so we spend most of this
    # function moving data into doc for the template to reference
    #

    option_names = []
    if 'options' in assertion_dict and assertion_dict['options']:
        for (k, v) in iteritems(assertion_dict['options']):
            # Error out if there's no description
            if 'description' not in assertion_dict['options'][k]:
                raise AnsibleError("Missing required description for option %s in %s " % (k, assertion_name))

            # Error out if required isn't a boolean (people have been putting
            # information on when something is required in here.  Those need
            # to go in the description instead).
            required_value = assertion_dict['options'][k].get('required', False)
            if not isinstance(required_value, bool):
                raise AnsibleError("Invalid required value '%s' for option '%s' in '%s' (must be truthy)" % (
                    required_value, k, assertion_name))

            # Make sure description is a list of lines for later formatting
            if not isinstance(assertion_dict['options'][k]['description'], list):
                assertion_dict['options'][k]['description'] = [assertion_dict['options'][k]['description']]
            option_names.append(k)
    option_names.sort()
    assertion_dict['option_keys'] = option_names

    assertion_dict['now_date'] = datetime.date.today().strftime('%Y-%m-%d')

    # here is where we build the table of contents...
    text = template.render(assertion_dict)
    print(text, file=out_file)


def main():
    env, template = jinja2_environment('.', 'assertion')
    assertions = read_docstring(ASSERTIONSFILE)

    out_file_path = os.path.join(OUTPUTDIR, "assertions.rst")
    out_file = open(out_file_path, "w")
    out_file.write('Assertions supported by bf_assert module\n')
    out_file.write('\n')

    out_file.write(".. contents::\n")
    out_file.write("   :local:\n")
    out_file.write("   :depth: 2\n")
    out_file.write('\n')


    for assertion_name in assertions["assertions"]:
        process_assertion(assertion_name, assertions["assertions"][assertion_name], template, out_file)

    out_file.close()


if __name__ == '__main__':
    main()
