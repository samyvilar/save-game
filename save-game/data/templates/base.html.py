# -*- encoding:utf-8 -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 6
_modified_time = 1300399882.784142
_template_filename=u'/home/cslab/csstudent/dura4262/repos/hg/SaveGameRepo/save-game/savegame/templates/base.html'
_template_uri=u'/base.html'
_template_cache=cache.Cache(__name__, _modified_time)
_source_encoding='utf-8'
from webhelpers.html import escape
_exports = ['base_meta', 'base_js', 'base_css', 'footer']


def render_body(context,**pageargs):
    context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u"<!DOCTYPE html>\n\n<html lang='en'>\n    <head>\n        ")
        # SOURCE LINE 5
        __M_writer(escape(self.title()))
        __M_writer(u'\n        ')
        # SOURCE LINE 6
        __M_writer(escape(self.base_meta()))
        __M_writer(u'\n        ')
        # SOURCE LINE 7
        __M_writer(escape(self.meta()))
        __M_writer(u'\n        ')
        # SOURCE LINE 8
        __M_writer(escape(self.base_css()))
        __M_writer(u'\n        ')
        # SOURCE LINE 9
        __M_writer(escape(self.css()))
        __M_writer(u'\n        ')
        # SOURCE LINE 10
        __M_writer(escape(self.base_js()))
        __M_writer(u'\n        ')
        # SOURCE LINE 11
        __M_writer(escape(self.js()))
        __M_writer(u"\n    </head>\n    <body>\n        <div id='container'>\n            ")
        # SOURCE LINE 15
        __M_writer(escape(self.header()))
        __M_writer(u'\n            ')
        # SOURCE LINE 16
        __M_writer(escape(self.body()))
        __M_writer(u'\n            ')
        # SOURCE LINE 17
        __M_writer(escape(self.footer()))
        __M_writer(u'\n        </div>\n    </body>\n\n</html>\n\n\n')
        # SOURCE LINE 26
        __M_writer(u'\n')
        # SOURCE LINE 29
        __M_writer(u'\n')
        # SOURCE LINE 32
        __M_writer(u'\n')
        # SOURCE LINE 37
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_base_meta(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 27
        __M_writer(u"\n    <meta http-equiv='Content-Type' content='text/html;charset=utf-8' />\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_base_js(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 33
        __M_writer(u"\n    <script\n    src='http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js'></script>\n\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_base_css(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 30
        __M_writer(u"\n    <link rel='stylesheet' href='/css/base.css' type='text/css' />\n")
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_footer(context):
    context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 24
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


