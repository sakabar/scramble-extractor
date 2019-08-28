from datetime import datetime
from typing import List, NamedTuple


class SolveResult(NamedTuple):
    is_dnf: bool
    total_sec: float
    multiphases: List[float]
    scramble: str
    datetime: datetime
