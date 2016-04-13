# -*- coding: utf-8 -*-

import pytest
from theoops.shells import Generic


class TestGeneric(object):
    @pytest.fixture
    def shell(self):
        return Generic()

    def test_from_shell(self, shell):
        assert shell.from_shell('pwd') == 'pwd'

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {}

    def test_app_alias(self, shell):
        assert 'alias oops' in shell.app_alias('oops')
        assert 'alias OOPS' in shell.app_alias('OOPS')
        assert 'theoops' in shell.app_alias('oops')
        assert 'TF_ALIAS=oops PYTHONIOENCODING' in shell.app_alias('oops')
        assert 'PYTHONIOENCODING=utf-8 theoops' in shell.app_alias('oops')

    def test_get_history(self, history_lines, shell):
        history_lines(['ls', 'rm'])
        # We don't know what to do in generic shell with history lines,
        # so just ignore them:
        assert list(shell.get_history()) == []

    def test_split_command(self, shell):
        assert shell.split_command('ls') == ['ls']
        assert shell.split_command(u'echo café') == [u'echo', u'café']
