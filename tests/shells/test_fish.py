# -*- coding: utf-8 -*-

import pytest
from theoops.shells import Fish


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestFish(object):
    @pytest.fixture
    def shell(self):
        return Fish()

    @pytest.fixture(autouse=True)
    def Popen(self, mocker):
        mock = mocker.patch('theoops.shells.fish.Popen')
        mock.return_value.stdout.read.return_value = (
            b'cd\nfish_config\noops\nfunced\nfuncsave\ngrep\nhistory\nll\nls\n'
            b'man\nmath\npopd\npushd\nruby')
        return mock

    @pytest.fixture
    def os_environ(self, monkeypatch, key, value):
        monkeypatch.setattr('os.environ', {key: value})

    @pytest.mark.parametrize('key, value', [
        ('TF_OVERRIDDEN_ALIASES', 'cut,git,sed'),  # legacy
        ('THEOOPS_OVERRIDDEN_ALIASES', 'cut,git,sed'),
        ('THEOOPS_OVERRIDDEN_ALIASES', 'cut, git, sed'),
        ('THEOOPS_OVERRIDDEN_ALIASES', ' cut,\tgit,sed\n'),
        ('THEOOPS_OVERRIDDEN_ALIASES', '\ncut,\n\ngit,\tsed\r')])
    def test_get_overridden_aliases(self, shell, os_environ):
        assert shell._get_overridden_aliases() == {'cd', 'cut', 'git', 'grep',
                                                   'ls', 'man', 'open', 'sed'}

    @pytest.mark.parametrize('before, after', [
        ('cd', 'cd'),
        ('pwd', 'pwd'),
        ('oops', 'fish -ic "oops"'),
        ('find', 'find'),
        ('funced', 'fish -ic "funced"'),
        ('grep', 'grep'),
        ('awk', 'awk'),
        ('math "2 + 2"', r'fish -ic "math \"2 + 2\""'),
        ('man', 'man'),
        ('open', 'open'),
        ('vim', 'vim'),
        ('ll', 'fish -ic "ll"'),
        ('ls', 'ls')])  # Fish has no aliases but functions
    def test_from_shell(self, before, after, shell):
        assert shell.from_shell(before) == after

    def test_to_shell(self, shell):
        assert shell.to_shell('pwd') == 'pwd'

    def test_and_(self, shell):
        assert shell.and_('foo', 'bar') == 'foo; and bar'

    def test_get_aliases(self, shell):
        assert shell.get_aliases() == {'fish_config': 'fish_config',
                                       'oops': 'oops',
                                       'funced': 'funced',
                                       'funcsave': 'funcsave',
                                       'history': 'history',
                                       'll': 'll',
                                       'math': 'math',
                                       'popd': 'popd',
                                       'pushd': 'pushd',
                                       'ruby': 'ruby'}

    def test_app_alias(self, shell):
        assert 'function oops' in shell.app_alias('oops')
        assert 'function OOPS' in shell.app_alias('OOPS')
        assert 'theoops' in shell.app_alias('oops')
        assert 'TF_ALIAS=oops PYTHONIOENCODING' in shell.app_alias('oops')
        assert 'PYTHONIOENCODING=utf-8 theoops' in shell.app_alias('oops')

    def test_get_history(self, history_lines, shell):
        history_lines(['- cmd: ls', '  when: 1432613911',
                       '- cmd: rm', '  when: 1432613916'])
        assert list(shell.get_history()) == ['ls', 'rm']
