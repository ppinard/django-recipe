""""""

# Standard library modules.

# Third party modules.
from django.forms.widgets import Textarea

# Local modules.

# Globals and constants variables.


class InstructionsTextWidget(Textarea):
    class Media:
        js = (
            "admin/js/jquery.init.js",
            "recipe/widgets/instructions.js",
        )

    template_name = "recipe/widgets/instructions.html"

    def __init__(self, attrs=None):
        default_attrs = {"class": "instructions"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
