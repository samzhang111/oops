from theoops.shells import shell
from theoops.utils import for_app


@for_app('tsuru')
def match(command):
    return ('not authenticated' in command.stderr
            and 'session has expired' in command.stderr)


def get_new_command(command):
    return shell.and_('tsuru login', command.script)
