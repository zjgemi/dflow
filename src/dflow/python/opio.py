import json
from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, List, Set, Union

import jsonpickle

from ..common import S3Artifact
from ..config import config
from ..io import PVC

ArtifactAllowedTypes = [str, Path, Set[str], Set[Path], List[str], List[Path]]


def type_to_str(type):
    if hasattr(type, "__module__") and hasattr(type, "__name__"):
        if type.__module__ == "builtins":
            return type.__name__
        else:
            return "%s.%s" % (type.__module__, type.__name__)
    else:
        return str(type)


class Artifact:
    """
    OPIO signature of artifact

    Args:
        type: str, Path, Set[str], Set[Path], List[str] or List[Path]
        archive: compress format of the artifact, None for no compression
        save: place to store the output artifact instead of default storage,
            can be a list
        optional: optional input artifact or not
        global_name: global name of the artifact within the workflow
    """

    def __init__(
            self,
            type: Any,
            archive: str = "default",
            save: List[Union[PVC, S3Artifact]] = None,
            optional: bool = False,
            global_name: str = None,
            sub_path: bool = True,
    ) -> None:
        self.type = type
        if archive == "default":
            archive = config["archive_mode"]
        self.archive = archive
        self.save = save
        self.optional = optional
        self.global_name = global_name
        self.sub_path = sub_path

    def __setattr__(self, key, value):
        if key == "type":
            assert (value in ArtifactAllowedTypes), "%s is not allowed" \
                                                    "artifact type, only %s " \
                                                    "are allowed." % (
                                                        value,
                                                        ArtifactAllowedTypes)
        super().__setattr__(key, value)

    def to_str(self):
        return "Artifact(type=%s, optional=%s, sub_path=%s)" % (
            type_to_str(self.type), self.optional, self.sub_path)


class Parameter:
    """
    OPIO signature of parameter

    Args:
        type: parameter type
        global_name: global name of the parameter within the workflow
        default: default value of the parameter
    """

    def __init__(
            self,
            type: Any,
            global_name: str = None,
            **kwargs,
    ) -> None:
        self.type = type
        self.global_name = global_name
        if "default" in kwargs:
            self.default = kwargs["default"]

    def to_str(self):
        default = ""
        if hasattr(self, "default"):
            try:
                default = ", default=%s" % json.dumps(self.default)
            except Exception:
                default = ", default=jsonpickle.loads('%s')" % \
                    jsonpickle.dumps(self.default)
        return "Parameter(type=%s%s)" % (type_to_str(self.type), default)


class BigParameter:
    """
    OPIO signature of big parameter

    Args:
        type: parameter type
    """

    def __init__(
            self,
            type: Any,
    ) -> None:
        self.type = type

    def to_str(self):
        return "BigParameter(type=%s)" % type_to_str(self.type)


class OPIOSign(MutableMapping):
    """The signature of OPIO.
    A signature of OPIO includes the key and its typing
    """

    def __init__(
            self,
            *args,
            **kwargs
    ):
        self._data = {}
        self._data = dict(*args, **kwargs)

    def __getitem__(
            self,
            key: str,
    ) -> Any:
        """Get the type hint of the key
        """
        return self._data[key]

    def __setitem__(
            self,
            key: str,
            value: Any,
    ) -> None:
        """Set the type hint of the key
        """
        self._data[key] = value

    def __delitem__(
            self,
            key: str,
    ) -> None:
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return str(self._data)


class OPIO(MutableMapping):
    def __init__(
            self,
            *args,
            **kwargs
    ):
        self._data = {}
        self._data = dict(*args, **kwargs)

    def __getitem__(
            self,
            key: str,
    ) -> Any:
        return self._data[key]

    def __setitem__(
            self,
            key: str,
            value: Any,
    ) -> None:
        self._data[key] = value

    def __delitem__(
            self,
            key: str,
    ) -> None:
        del self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return str(self._data)
