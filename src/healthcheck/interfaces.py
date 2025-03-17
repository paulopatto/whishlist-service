from dataclasses import dataclass
from typing import Protocol


class IHealthCheckResult(Protocol):
    health: bool
    message: str

@dataclass
class HealthCheckResultDTO:
    health: bool
    message: str
