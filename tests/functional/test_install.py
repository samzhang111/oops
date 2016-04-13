import pytest
from theoops.utils import get_installation_info

envs = ((u'bash', 'theoops/ubuntu-bash', u'''
FROM ubuntu:latest
RUN apt-get update
RUN apt-get install -yy bash
'''), (u'bash', 'theoops/generic-bash', u'''
FROM fedora:latest
RUN dnf install -yy python-devel sudo wget gcc
'''))


@pytest.mark.functional
@pytest.mark.skip_without_docker
@pytest.mark.parametrize('shell, tag, dockerfile', envs)
def test_installation(spawnu, shell, TIMEOUT, tag, dockerfile):
    proc = spawnu(tag, dockerfile, shell)
    proc.sendline(u'cat /src/install.sh | sh - && $0')
    proc.sendline(u'theoops --version')
    version = get_installation_info().version
    assert proc.expect([TIMEOUT, u'theoops {}'.format(version)],
                       timeout=600)
    proc.sendline(u'oops')
    assert proc.expect([TIMEOUT, u'No oopss given'])
