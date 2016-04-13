# -*- coding: utf-8 -*-

import os
import pytest
from theoops.shells.zsh import Zsh


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestZsh(object):
    @pytest.fixture
    def shell(self):
        return Zsh()

    @pytest.fixture(autouse=True)
    def shell_aliases(self):
        os.environ['TF_SHELL_ALIASES'] = (
            'oops=\'eval $(theoops $(fc -ln -1 | tail -n 1))\'\n'
            'l=\'ls -CF\'\n'
            'la=\'ls -A\'\n'
            'll=\'ls -alF\'')

    @pytest.mark.parametrize('before, after', [
        ('oops', 'eval $(theoops $(fc -ln -1 | tail -n 1))'),
        ('pwd', 'pwd'),
        ('ll', 'ls -alF')])
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == 'ls && cd'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {
            'oops': 'eval $(theoops $(fc -ln -1 | tail -n 1))',
            'l': 'ls -CF',
            'la': 'ls -A',
            'll': 'ls -alF'}

    def test_app_alias(self, shell):
        assert 'alias oops' in shell.app_alias('oops')
        assert 'alias OOPS' in shell.app_alias('OOPS')
        assert 'theoops' in shell.app_alias('oops')
        assert 'PYTHONIOENCODING' in shell.app_alias('oops')

    def test_app_alias_variables_correctly_set(self, shell):
        alias = shell.app_alias('oops')
        assert "alias oops='TF_CMD=$(TF_ALIAS" in alias
        assert '$(TF_ALIAS=oops PYTHONIOENCODING' in alias
        assert 'PYTHONIOENCODING=utf-8 TF_SHELL_ALIASES' in alias
        assert 'ALIASES=$(alias) theoops' in alias

    def test_get_history(self, history_lines, shell):
        history_lines([': 1432613911:0;ls', ': 1432613916:0;rm'])
        assert list(shell.get_history()) == ['ls', 'rm']
