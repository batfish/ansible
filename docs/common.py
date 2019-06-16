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

import re

from jinja2 import Environment, FileSystemLoader

try:
    from html import escape as html_escape
except ImportError:
    # Python-3.2 or later
    import cgi

    def html_escape(text, quote=True):
        return cgi.escape(text, quote)

__all__ = ['jinja2_environment', 'html_ify', 'rst_fmt', 'rst_ify', 'rst_xline']


_ITALIC = re.compile(r"I\(([^)]+)\)")
_BOLD = re.compile(r"B\(([^)]+)\)")
_MODULE = re.compile(r"M\(([^)]+)\)")
_URL_W_TEXT = re.compile(r"U\(([^)^|]+)\|([^)]+)\)")
_URL = re.compile(r"U\(([^)^|]+)\)")
_CONST = re.compile(r"C\(([^)]+)\)")
_UNDERSCORE = re.compile(r"_")


def module_to_html(matchobj):
    if matchobj.group(1) is not None:
        module_name = matchobj.group(1)
        module_href = _UNDERSCORE.sub('-', module_name)
        return '<a class="reference internal" href="#' + module_href + '"><span class="std std-ref">' + \
                    module_name + '</span></a>'
    return ''


def html_ify(text):
    ''' convert symbols like I(this is in italics) to valid HTML '''

    t = html_escape(text)
    t = _ITALIC.sub("<em>" + r"\1" + "</em>", t)
    t = _BOLD.sub("<b>" + r"\1" + "</b>", t)
    t = _MODULE.sub(module_to_html, t)
    t = _URL_W_TEXT.sub("<a href='" + r"\2" + "'>" + r"\1" + "</a>", t)
    t = _URL.sub("<a href='" + r"\1" + "'>" + r"\1" + "</a>", t)
    t = _CONST.sub("<code>" + r"\1" + "</code>", t)

    return t


def rst_xline(width, char="="):
    ''' return a restructured text line of a given length '''

    return char * width


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


def jinja2_environment(template_dir, template_type, template_file_name):

    env = Environment(loader=FileSystemLoader(template_dir),
                      variable_start_string="@{",
                      variable_end_string="}@",
                      trim_blocks=True,
                      )
    env.globals['xline'] = rst_xline

    if template_type == 'rst':
        env.filters['convert_symbols_to_format'] = rst_ify
        env.filters['html_ify'] = html_ify
        env.filters['fmt'] = rst_fmt
        env.filters['xline'] = rst_xline
        template = env.get_template(template_file_name)
        outputname = "%s.rst"
    else:
        raise Exception("unknown format type: %s" % template_type)

    return env, template, outputname

