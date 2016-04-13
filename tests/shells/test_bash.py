# -*- coding: utf-8 -*-

import os
import pytest
from theoops.shells import Bash


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestBash(object):
    @pytest.fixture
    def shell(self):
        return Bash()

    @pytest.fixture(autouse=True)
    def shell_aliases(self):
        os.environ['TF_SHELL_ALIASES'] = (
            'alias oops=\'eval $(theoops $(fc -ln -1))\'\n'
            'alias l=\'ls -CF\'\n'
            'alias la=\'ls -A\'\n'
            'alias ll=\'ls -alF\'')

    @pytest.mark.parametrize('before, after', [
        ('pwd', 'pwd'),
        ('oops', 'eval $(theoops $(fc -ln -1))'),
        ('awk', 'awk'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'oops': 'eval $(theoops $(fc -ln -1))',
                                       'l': 'ls -CF',
                                       'la': 'ls -A',
                                       'll': 'ls -alF'}

    def test_app_alias(self, shell):
        assert 'alias oops' in shell.app_alias('oops')
        assert 'alias OOPS' in shell.app_alias('OOPS')
        assert 'theoops' in shell.app_alias('oops')
        assert 'TF_ALIAS=oops' in shell.app_alias('oops')
        assert 'PYTHONIOENCODING=utf-8' in shell.app_alias('oops')

    def test_app_alias_variables_correctly_set(self, shell):
        alias = shell.app_alias('oops')
        assert "alias oops='TF_CMD=$(TF_ALIAS" in alias
        assert '$(TF_ALIAS=oops PYTHONIOENCODING' in alias
        assert 'PYTHONIOENCODING=utf-8 TF_SHELL_ALIASES' in alias
        assert 'ALIASES=$(alias) theoops' in alias

    def test_get_history(self, history_lines, shell):
        history_lines(['ls', 'rm'])
        assert list(shell.get_history()) == ['ls', 'rm']
