import dataclasses
from typing import Callable


@dataclasses.dataclass
class ArtifactInfo:
    name: str
    size: int
    files_count: int


@dataclasses.dataclass
class ArchiverInfo:
    name: str
    extract: Callable


@dataclasses.dataclass
class ExecutionInfo:
    execution_time: float
    artifact: ArtifactInfo
    archiver: str
