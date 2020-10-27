"""WIP to add a gtin extension type for usage with pandas."""

import numpy as np
from pandas.api.extensions import (
    ExtensionDtype, ExtensionArray, register_extension_dtype
)

from gtin import GTIN


@register_extension_dtype
class GTINDtype(ExtensionDtype):
    @property
    def name(self):
        return "gtin"

    @property
    def type(self):
        """The scalar type."""
        return GTIN

    @classmethod
    def construct_from_string(cls, string):
        if string == cls.name:
            return cls()
        else:
            raise TypeError("Cannot construct a '{}' from "
                            "'{}'".format(cls, string))


class GTINArray(ExtensionArray):

    def __init__(self, gtins):
        self._data = gtins

    def __array__(self, dtype=None):
        # This is required
        # See https://github.com/pandas-dev/pandas/issues/24858
        return self._data

    @property
    def dtype(self):
        return GTINDtype()

    @classmethod
    def _from_sequence(cls, scalars, dtype=object):
        return cls(scalars, dtype=dtype)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._data[key]
        else:
            return GTINArray(self._data[key])

    # def __getitem__(self, *args):
    #     result = operator.getitem(self.data, *args)
    #     return result

    def __setitem__(self, key, value):
        self.data[key] = value  # GTINArray([value])

    def isna(self):
        return np.array([val is None for val in self._data], dtype=bool)


# TODO: Move this example, once working
if __name__ == "__main__":
    import pandas as pd

    from gtin import GTIN

    df = pd.DataFrame({
        'geoms': GTINArray(
            np.array(
                [GTIN(123456789012), GTIN("938475601234")],
                dtype=object)
        )
    })
    repr(df)
