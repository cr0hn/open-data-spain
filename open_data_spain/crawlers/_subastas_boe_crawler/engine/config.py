from dataclasses import dataclass


@dataclass
class RunningConfig:
    log_level: str = "INFO"
    global_max_count: int = -1
    max_per_territory: int = 50


__all__ = ("RunningConfig", )
