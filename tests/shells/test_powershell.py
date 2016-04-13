# -*- coding: utf-8 -*-

import pytest
from theoops.shells import Powershell


@pytest.mark.usefixtures('isfile', 'no_memoize', 'no_cache')
class TestPowershell(object):
    @pytest.fixture
    def shell(self):
        return Powershell()

    def test_and_(self, shell):
        assert shell.and_('ls', 'cd') == '(ls) -and (cd)'

    def test_app_alias(self, shell):
        assert 'function oops' in shell.app_alias('oops')
        assert 'function OOPS' in shell.app_alias('OOPS')
        assert 'theoops' in shell.app_alias('oops')
