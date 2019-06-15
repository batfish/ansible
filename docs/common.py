import re
from jinja2 import Environment, FileSystemLoader

__all__ = ['jinja2_environment']


_ITALIC = re.compile(r"I\(([^)]+)\)")
_BOLD = re.compile(r"B\(([^)]+)\)")
_MODULE = re.compile(r"M\(([^)]+)\)")
_URL_W_TEXT = re.compile(r"U\(([^)^|]+)\|([^)]+)\)")
_URL = re.compile(r"U\(([^)^|]+)\)")
_CONST = re.compile(r"C\(([^)]+)\)")
_UNDERSCORE = re.compile(r"_")

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

#####################################################################################


def rst_fmt(text, fmt):
    ''' helper for Jinja2 to do format strings '''

    return fmt % (text)

#####################################################################################


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

    if template_type == 'rst':
        env.filters['convert_symbols_to_format'] = rst_ify
        env.filters['html_ify'] = html_ify
        env.filters['fmt'] = rst_fmt
        env.filters['xline'] = rst_xline
        template = env.get_template('rst.j2')
        outputname = "%s.rst"
    else:
        raise Exception("unknown module format type: %s" % template_type)

    return env, template, outputname

