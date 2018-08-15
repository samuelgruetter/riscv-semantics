#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by TatSu.
#
#    https://pypi.python.org/pypi/tatsu/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from tatsu.buffering import Buffer
from tatsu.parsing import Parser
from tatsu.parsing import tatsumasu
from tatsu.util import re, generic_main  # noqa


KEYWORDS = {}  # type: ignore


class TinyHaskellBuffer(Buffer):
    def __init__(
        self,
        text,
        whitespace=None,
        nameguard=None,
        comments_re='{-((?:.|\\n)*?)-}',
        eol_comments_re='--([^\\n]*?)$',
        ignorecase=None,
        namechars='',
        **kwargs
    ):
        super(TinyHaskellBuffer, self).__init__(
            text,
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            namechars=namechars,
            **kwargs
        )


class TinyHaskellParser(Parser):
    def __init__(
        self,
        whitespace=None,
        nameguard=None,
        comments_re='{-((?:.|\\n)*?)-}',
        eol_comments_re='--([^\\n]*?)$',
        ignorecase=None,
        left_recursion=True,
        parseinfo=True,
        keywords=None,
        namechars='',
        buffer_class=TinyHaskellBuffer,
        **kwargs
    ):
        if keywords is None:
            keywords = KEYWORDS
        super(TinyHaskellParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            comments_re=comments_re,
            eol_comments_re=eol_comments_re,
            ignorecase=ignorecase,
            left_recursion=left_recursion,
            parseinfo=parseinfo,
            keywords=keywords,
            namechars=namechars,
            buffer_class=buffer_class,
            **kwargs
        )

    @tatsumasu()
    def _start_(self):  # noqa
        self._module_()
        self._check_eof()

    @tatsumasu('Module')
    def _module_(self):  # noqa
        self._token('module')
        self._modid_()
        self.name_last_node('name')
        self._token('where')
        self._impdecls_()
        self.name_last_node('imports')
        self._topdecls_()
        self.name_last_node('decls')
        self.ast._define(
            ['decls', 'imports', 'name'],
            []
        )

    @tatsumasu()
    def _impdecls_(self):  # noqa

        def block0():
            self._impdecl_()
        self._closure(block0)

    @tatsumasu()
    def _topdecls_(self):  # noqa

        def block0():
            self._topdecl_()
        self._closure(block0)

    @tatsumasu()
    def _impdecl_(self):  # noqa
        self._token('import')
        self._modid_()
        self.name_last_node('@')

    @tatsumasu()
    def _topdecl_(self):  # noqa
        with self._choice():
            with self._option():
                self._typedecl_()
            with self._option():
                self._datadecl_()
            self._error('no available options')

    @tatsumasu('TypeDecl')
    def _typedecl_(self):  # noqa
        self._token('type')
        self._simpletype_()
        self.name_last_node('name')
        self._token('=')
        self._type_()
        self.name_last_node('rhs')
        self.ast._define(
            ['name', 'rhs'],
            []
        )

    @tatsumasu('ADTDecl')
    def _datadecl_(self):  # noqa
        self._token('data')
        self._simpletype_()
        self.name_last_node('name')
        self._token('=')
        self._constrs_()
        self.name_last_node('constructors')
        with self._optional():
            self._deriving_()
        self.ast._define(
            ['constructors', 'name'],
            []
        )

    @tatsumasu()
    def _simpletype_(self):  # noqa
        self._tycon_()

    @tatsumasu()
    def _type_(self):  # noqa
        self._tycon_()

    @tatsumasu()
    def _tycon_(self):  # noqa
        self._conid_()

    @tatsumasu()
    def _tycls_(self):  # noqa
        self._conid_()

    @tatsumasu()
    def _constrs_(self):  # noqa

        def sep0():
            self._token('|')

        def block0():
            self._constr_()
        self._positive_gather(block0, sep0)

    @tatsumasu('Constructor')
    def _constr_(self):  # noqa
        self._conid_()
        self.name_last_node('name')
        self._fielddecls_()
        self.name_last_node('args')
        self.ast._define(
            ['args', 'name'],
            []
        )

    @tatsumasu()
    def _fielddecls_(self):  # noqa
        with self._choice():
            with self._option():
                self._token('{')

                def sep0():
                    self._token(',')

                def block0():
                    self._fielddecl_()
                self._gather(block0, sep0)
                self._token('}')
            with self._option():
                self._empty_closure()
            self._error('no available options')

    @tatsumasu('FieldDecl')
    def _fielddecl_(self):  # noqa
        self._varid_()
        self.name_last_node('name')
        self._token('::')
        self._type_()
        self.name_last_node('type')
        self.ast._define(
            ['name', 'type'],
            []
        )

    @tatsumasu()
    def _deriving_(self):  # noqa
        self._token('deriving')
        self._token('(')

        def sep0():
            self._token(',')

        def block0():
            self._tycls_()
        self._gather(block0, sep0)
        self._token(')')

    @tatsumasu('str')
    def _modid_(self):  # noqa
        self._pattern(r'[A-Z][a-z_A-Z0-9]*(\.[A-Z][a-z_A-Z0-9]*)*')

    @tatsumasu('str')
    def _conid_(self):  # noqa
        self._pattern(r'[A-Z][a-z_A-Z0-9]*')

    @tatsumasu('str')
    def _varid_(self):  # noqa
        self._pattern(r'[a-z_][a-z_A-Z0-9]*')


class TinyHaskellSemantics(object):
    def start(self, ast):  # noqa
        return ast

    def module(self, ast):  # noqa
        return ast

    def impdecls(self, ast):  # noqa
        return ast

    def topdecls(self, ast):  # noqa
        return ast

    def impdecl(self, ast):  # noqa
        return ast

    def topdecl(self, ast):  # noqa
        return ast

    def typedecl(self, ast):  # noqa
        return ast

    def datadecl(self, ast):  # noqa
        return ast

    def simpletype(self, ast):  # noqa
        return ast

    def type(self, ast):  # noqa
        return ast

    def tycon(self, ast):  # noqa
        return ast

    def tycls(self, ast):  # noqa
        return ast

    def constrs(self, ast):  # noqa
        return ast

    def constr(self, ast):  # noqa
        return ast

    def fielddecls(self, ast):  # noqa
        return ast

    def fielddecl(self, ast):  # noqa
        return ast

    def deriving(self, ast):  # noqa
        return ast

    def modid(self, ast):  # noqa
        return ast

    def conid(self, ast):  # noqa
        return ast

    def varid(self, ast):  # noqa
        return ast


def main(filename, start=None, **kwargs):
    if start is None:
        start = 'start'
    if not filename or filename == '-':
        text = sys.stdin.read()
    else:
        with open(filename) as f:
            text = f.read()
    parser = TinyHaskellParser()
    return parser.parse(text, rule_name=start, filename=filename, **kwargs)


if __name__ == '__main__':
    import json
    from tatsu.util import asjson

    ast = generic_main(main, TinyHaskellParser, name='TinyHaskell')
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(asjson(ast), indent=2))
    print()
