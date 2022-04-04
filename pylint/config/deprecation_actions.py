# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/main/LICENSE
# Copyright (c) https://github.com/PyCQA/pylint/blob/main/CONTRIBUTORS.txt

# pylint: disable=too-many-arguments, redefined-builtin

"""Deprecated option actions."""

import argparse
import warnings
from typing import Any, List, Optional, Sequence, Union


class _OldNamesAction(argparse._StoreAction):
    """Store action that also sets the value to old names."""

    def __init__(
        self,
        option_strings: Sequence[str],
        dest: str,
        nargs: None = None,
        const: None = None,
        default: None = None,
        type: None = None,
        choices: None = None,
        required: bool = False,
        help: str = "",
        metavar: str = "",
        old_names: Optional[List[str]] = None,
    ) -> None:
        assert old_names
        self.old_names = old_names
        super().__init__(
            option_strings,
            dest,
            "+",
            const,
            default,
            type,
            choices,
            required,
            help,
            metavar,
        )

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ):
        assert isinstance(values, list)
        setattr(namespace, self.dest, values[0])
        for old_name in self.old_names:
            setattr(namespace, old_name, values[0])


class _NewNamesAction(argparse._StoreAction):
    """Store action that also emits a deprecation warning about a new name."""

    def __init__(
        self,
        option_strings: Sequence[str],
        dest: str,
        nargs: None = None,
        const: None = None,
        default: None = None,
        type: None = None,
        choices: None = None,
        required: bool = False,
        help: str = "",
        metavar: str = "",
        new_names: Optional[List[str]] = None,
    ) -> None:
        assert new_names
        self.new_names = new_names
        super().__init__(
            option_strings,
            dest,
            "+",
            const,
            default,
            type,
            choices,
            required,
            help,
            metavar,
        )

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ):
        assert isinstance(values, list)
        setattr(namespace, self.dest, values[0])
        warnings.warn(
            f"{self.option_strings[0]} has been deprecated. Please look into "
            f"using any of the following options: {', '.join(self.new_names)}.",
            DeprecationWarning,
        )
