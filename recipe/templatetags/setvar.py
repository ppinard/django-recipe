""""""

# Standard library modules.

# Third party modules.
from django import template

# Local modules.

# Globals and constants variables.


register = template.Library()


@register.simple_tag
def setvar(val=None):
    return val
