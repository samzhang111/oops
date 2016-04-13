class EmptyCommand(Exception):
    """Raised when empty command passed to `theoops`."""


class NoRuleMatched(Exception):
    """Raised when no rule matched for some command."""
