from typing import Tuple, Union

import numpy as np


def stringify_upc(upc) -> Tuple[str, bool]:
    # Convert any non NaN or inf to a string
    if np.isfinite(upc):
        return str(int(upc)), True
    elif isinstance(upc, str):
        return str(int(re.sub(r"[^0-9.]", "", upc))), True

    return upc, False


def is_valid_gtin():
    pass


def add_check_digit():
    pass


def has_aald():
    pass


def remove_invalid_chars(gtin, invalid_chars=None):
    pass


def diagnose_upc():
    pass


def format_as_upc_a():
    pass


def format_as_gtin12():
    pass


def format_as_gtin13():
    pass


def format_as_gtin14():
    pass


class GTIN:
    """
    The GTIN standard has incorporated the
    International Standard Book Number (ISBN),
    International Standard Serial Number (ISSN),
    International Standard Music Number (ISMN),
    International Article Number (which includes the European Article Number and Japanese Article Number)
    and some Universal Product Codes (UPCs),
    into a universal number space.

    GTINs may be 8, 12, 13 or 14 digits long,
    and each of these four numbering structures are constructed in a similar fashion,
    combining Company Prefix, Item Reference, and a calculated Check Digit
    (GTIN-14 adds another component- the Indicator Digit, which can be 1-8).
    The most commonly used encodings in retail are: UPC-A, EAN-13, EAN-8, and UPC-E.

    """
    SUPPORTED_TYPES = {
        "GTIN-8": format_as_upc_a,      # AKA EAN-8
        "GTIN-12": format_as_gtin12,    # AKA EAN-12
        "GTIN-13": format_as_gtin13,    # AKA EAN-13
        "GTIN-14": format_as_gtin14,    # AKA EAN-14
    }

    def __init__(self, original_code: Union[str, int], has_check_digit: bool = None):
        self.original_code = original_code
        self.has_check_digit = has_check_digit  # TODO: add infer and check option
        self._eq_code = None  # Internal representation for efficient comparison

        # These are all set by calling `self.format_as(code_type)`
        self._display_code_type = None
        self.display_code = None

        self.is_valid = None
        self.invalid_reason = None

    @property
    def display_code_type(self):
        return self._display_code_type

    @display_code_type.setter
    def display_code_type(self, display_code_type):
        if not display_code_type in self.SUPPORTED_TYPES:
            raise ValueError(f"{self.display_code_type} is not a valid GTIN type. "
                             f"Please choose from {', '.join(self.SUPPORTED_TYPES)}")
        self._display_code_type = display_code_type

    def __len__(self):
        return len(self.original_code)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.original_code!r}, "
            f"has_check_digit={self.has_check_digit!r})"
        )

    def __str__(self):
        # TODO: fix this
        return f"{self.display_code!r}" or f"{self.original_code!r}"

    def __eq__(self, other):
        if not isinstance(other, ProductCode):
            return NotImplemented
        return self._eq_code == other._eq_code

    def format_as(self, code_type):
        self.display_code_type = code_type
        formatting_func = self.SUPPORTED_TYPES.get(code_type)
        if formatting_func is None:
            self.is_valid = False
            self.invalid_reason = e
            return

        try:
            self.display_code = formatting_func(self.original_code)
            self.is_valid = True
        # TODO: Narrow this exception
        except Exception as e:
            self.display_code = self.original_code
            self.is_valud = False
            self.invalid_reason = e
