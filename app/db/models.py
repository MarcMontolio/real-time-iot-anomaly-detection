from app.db.base import Base

from app.models.device import Device  # noqa: F401
from app.models.telemetry_event import TelemetryEvent  # noqa: F401

__all__ = ["Base"]