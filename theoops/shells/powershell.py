from .generic import Generic


class Powershell(Generic):
    def app_alias(self, oops):
        return 'function ' + oops + ' { \n' \
               '    $oops = $(theoops (Get-History -Count 1).CommandLine)\n' \
               '    if (-not [string]::IsNullOrWhiteSpace($oops)) {\n' \
               '        if ($oops.StartsWith("echo")) { $oops = $oops.Substring(5) }\n' \
               '        else { iex "$oops" }\n' \
               '    }\n' \
               '}\n'

    def and_(self, *commands):
        return u' -and '.join('({0})'.format(c) for c in commands)

    def how_to_configure(self):
        return 'iex "theoops --alias"', '$profile'
