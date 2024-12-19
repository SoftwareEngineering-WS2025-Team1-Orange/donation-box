from dataclasses import dataclass
from typing import List

from bright_ws.annotations.classes.lifecycle import Lifecycle
from bright_ws.annotations.classes.router import Router


@dataclass
class BrightConfig:
    host_url: str
    routes: List[Router]
    lifecycle: List[Lifecycle]
