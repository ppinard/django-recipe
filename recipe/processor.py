""""""

# Standard library modules.
import re
import collections
import xml.etree.ElementTree as etree
import math

# Third party modules.
from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import InlineProcessor
from markdown.extensions import Extension

from django.conf import settings
from loguru import logger
import humanize
import pint

ureg = pint.UnitRegistry()
ureg.define("pinch = 0.36 g")


# Local modules.

# Globals and constants variables.
UnitDefinition = collections.namedtuple("UnitDefinition", ["vmin", "vmax", "digits"])
DEFINITION_PATTERN = re.compile(
    r"\[(?P<quantity>[\d\.]+)\]\(?(?P<unit>.*?)?\)?\[(?P<name>.*?)\]"
)


class RecipeProcessorError(Exception):
    pass


class NoUnitDefinitionError(RecipeProcessorError):
    def __init__(self, unit):
        super().__init__(f"No definition for {unit}")
        self.unit = unit


class UnitConversionError(RecipeProcessorError):
    def __init__(self, from_unit, to_unit):
        super().__init__(f"Cannot convert {from_unit} to {to_unit}")
        self.from_unit = from_unit
        self.to_unit = to_unit


class UnitMismatchError(RecipeProcessorError):
    def __init__(self, expected_unit):
        super().__init__(
            f"Mismatch with ingredient units. Expected unit {expected_unit:~P}"
        )
        self.expected_unit = expected_unit


class UnknownUnitError(RecipeProcessorError):
    def __init__(self, unit):
        super().__init__(f"Unknown unit {unit}")
        self.unit = unit


class IngredientList:
    def __init__(self, unit_definitions, unit_conversions):
        self.conversions = {}
        self.densities = {}
        for item in unit_conversions:
            for name in item["names"]:
                self.conversions[name] = item["units"]
                self.densities[name] = item["density"] * ureg("g/cm^3")

        default = UnitDefinition(0.0, float("inf"), 10)
        self.definitions = collections.defaultdict(lambda: default)
        for unit, item in unit_definitions.items():
            vmin = item.get("min", default.vmin)
            vmax = item.get("max", default.vmax)
            digits = item.get("digits", 10)
            self.definitions[unit] = UnitDefinition(vmin, vmax, digits)

        self.ingredients = {}
        self.errors = []

    def _log_error(self, error):
        self.errors.append(error)
        logger.error(str(error))

    def _create_quantity_text(self, quantity, unit):
        definition = self.definitions[unit]

        # Round value
        quantity = round(quantity, definition.digits)

        # Create text
        quantity_str = humanize.fractional(quantity)
        unit = ureg(unit).units
        return f"{quantity_str} {unit:~P}"

    def _create_equivalences(self, name, uquantity):
        equivalences = []
        for unit in self.conversions[name]:
            if unit not in self.definitions:
                error = NoUnitDefinitionError(unit)
                self._log_error(error)
                continue

            try:
                equivalent_quantity = uquantity.to(unit)
            except pint.DimensionalityError:
                if uquantity.check("[mass]") and name in self.densities:
                    equivalent_quantity = (uquantity / self.densities[name]).to(unit)
                elif uquantity.check("[length] ** 3") and name in self.densities:
                    equivalent_quantity = (uquantity * self.densities[name]).to(unit)
                else:
                    error = UnitConversionError(uquantity.units, unit)
                    self._log_error(error)
                    continue

            # Check acceptable range
            definition = self.definitions[unit]
            magnitude = equivalent_quantity.magnitude
            if magnitude < definition.vmin or magnitude > definition.vmax:
                continue

            quantity_text = self._create_quantity_text(magnitude, unit)
            equivalences.append(quantity_text)

        return equivalences

    def add_ingredient(self, name, quantity, unit=None):
        quantity = float(quantity)

        # No unit
        if not unit:
            self.ingredients.setdefault(name, 0.0)

            try:
                self.ingredients[name] += ureg.Quantity(quantity)
            except:
                other_unit = self.ingredients[name].units
                error = UnitMismatchError(other_unit)
                self._log_error(error)
                return f"!!!error {error}"

            quantity_text = humanize.fractional(quantity)
            return f"*{name}* ({quantity_text})"

        # Create quantity
        try:
            uquantity = quantity * ureg(unit)
        except:
            error = UnknownUnitError(unit)
            self._log_error(error)
            return f"!!!error {error}"

        # Convert to quantity to mass, if possible
        if uquantity.check("[mass]") and name in self.densities:
            uquantity = uquantity / self.densities[name]

        # Add to ingredients
        self.ingredients.setdefault(name, 0.0 * uquantity.units)

        try:
            self.ingredients[name] += uquantity
        except:
            other_unit = self.ingredients[name].units
            error = UnitMismatchError(other_unit)
            self._log_error(error)
            return f"!!!error {error}"

        # No conversion for this ingredient
        if name not in self.conversions:
            quantity_text = self._create_quantity_text(quantity, unit)
            return f"*{name}* ({quantity_text})"

        # Apply conversion
        equivalences = self._create_equivalences(name, uquantity)
        return f"*{name}* (" + " | ".join(equivalences) + ")"

    def get_lines(self):
        lines = []

        for name, uquantity in sorted(self.ingredients.items()):
            if uquantity.dimensionless:
                quantity_text = humanize.fractional(uquantity.magnitude)

            elif name not in self.conversions:
                quantity_text = self._create_quantity_text(
                    uquantity.magnitude, str(uquantity.units)
                )

            else:
                equivalences = self._create_equivalences(name, uquantity)
                quantity_text = " | ".join(equivalences)

            lines.append(f"* {name}: {quantity_text}")

        lines.append("")
        return lines


class RecipePreprocessor(Preprocessor):
    def __init__(
        self, unit_definitions, unit_conversions, output_ingredient_list=True, md=None
    ):
        super().__init__(md)
        self.ingredientlist = IngredientList(unit_definitions, unit_conversions)
        self.output_ingredient_list = output_ingredient_list

    def run(self, lines):
        # Process lines
        newlines = []
        for line in lines:
            while True:
                match = DEFINITION_PATTERN.search(line)
                if not match:
                    break

                # Create ingredient
                quantity, unit, name = match.groups()
                text = self.ingredientlist.add_ingredient(name, quantity, unit)
                logger.debug(
                    f"start={match.start(0)}, end={match.end(0)}, quantity={quantity}, unit={unit}, name={name}"
                )

                # Create text
                line = line[: match.start(0)] + text + line[match.end(0) :]

            newlines.append(line)
        else:
            newlines.append(line)

        # Create output lines
        outlines = []
        if self.output_ingredient_list:
            outlines += ["# Ingredients", ""]
            outlines += self.ingredientlist.get_lines()
            outlines += ["# Instructions", ""]

        outlines += newlines

        return outlines


class TemperatureInlineProcessor(InlineProcessor):
    def __init__(self, md=None):
        pattern = r"\((?P<temperature>\d+)\)\[(?P<unit>[CF]?)\]"
        super().__init__(pattern, md)

    def handleMatch(self, match, data):
        temperature, unit = match.groups()

        if unit not in ["C", "F"]:
            el = etree.Element("span")
            el.text = f"!!!error unknown temperature unit {unit}"
            return el, match.start(0), match.end(0)

        temperature = int(float(temperature))
        if unit == "C":
            unit = "degC"
        elif unit == "F":
            unit = "degF"

        uquantity = ureg.Quantity(temperature, unit)

        # Calculate equivalences
        equivalences = []

        equivalences.append(f"{uquantity.to('degC').magnitude:.0f} &deg;C")
        equivalences.append(f"{uquantity.to('degF').magnitude:.0f} &deg;F")

        gasmark = max(1, math.ceil((uquantity.to("degC").magnitude - 121) / 14))
        equivalences.append(f"Gas {gasmark}")

        el = etree.Element("span")
        el.text = " | ".join(equivalences)
        return el, match.start(0), match.end(0)


class RecipeExtension(Extension):
    def __init__(
        self, unit_definitions, unit_conversions, output_ingredient_list=True, **kwargs
    ):
        super().__init__(**kwargs)
        self.unit_definitions = unit_definitions
        self.unit_conversions = unit_conversions
        self.output_ingredient_list = output_ingredient_list

    def extendMarkdown(self, md):
        self.recipe_processor = RecipePreprocessor(
            self.unit_definitions,
            self.unit_conversions,
            self.output_ingredient_list,
            md,
        )
        md.preprocessors.register(self.recipe_processor, "recipe", 12)

        self.temperature_processor = TemperatureInlineProcessor(md)
        md.inlinePatterns.register(self.temperature_processor, "temp", 175)


MARKDOWN_EXT = RecipeExtension(
    getattr(settings, "RECIPE_UNIT_DEFINITIONS", {}),
    getattr(settings, "RECIPE_UNIT_CONVERSIONS", []),
    output_ingredient_list=True,
)

MARKDOWN_EXT_PREVIEW = RecipeExtension(
    getattr(settings, "RECIPE_UNIT_DEFINITIONS", {}),
    getattr(settings, "RECIPE_UNIT_CONVERSIONS", []),
    output_ingredient_list=False,
)
