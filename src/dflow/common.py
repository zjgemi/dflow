from copy import deepcopy
from typing import Any, Union

from .config import s3_config

try:
    from argo.workflows.client import V1alpha1OSSArtifact, V1alpha1S3Artifact
    from argo.workflows.client.configuration import Configuration
except Exception:
    V1alpha1S3Artifact = object


class S3Artifact(V1alpha1S3Artifact):
    """
    S3 artifact

    Args:
        key: key of the s3 artifact
    """

    def __init__(
            self,
            path_list: Union[str, list] = None,
            *args,
            **kwargs,
    ) -> None:
        config = Configuration()
        config.client_side_validation = False
        super().__init__(local_vars_configuration=config, *args, **kwargs)
        assert isinstance(self.key, str)
        if not self.key.startswith(s3_config["prefix"]):
            self.key = s3_config["prefix"] + self.key
        if path_list is None:
            path_list = []
        self.path_list = path_list

    def to_dict(self):
        d = {"key": self.key}
        if s3_config["storage_client"] is None:
            d.update(s3_config)
        else:
            d.update(s3_config["storage_client"].to_dict())
        return d

    @classmethod
    def from_dict(cls, d):
        return cls(key=d["key"])

    def sub_path(
            self,
            path: str,
    ) -> Any:
        artifact = deepcopy(self)
        if artifact.key[-1:] != "/":
            artifact.key += "/"
        artifact.key += path
        return artifact

    def download(self, **kwargs):
        from .utils import download_artifact
        download_artifact(self, **kwargs)

    def oss(self):
        config = Configuration()
        config.client_side_validation = False
        return V1alpha1OSSArtifact(key=s3_config["repo_prefix"] + self.key,
                                   local_vars_configuration=config)


class LocalArtifact:
    def __init__(self, local_path):
        self.local_path = local_path
