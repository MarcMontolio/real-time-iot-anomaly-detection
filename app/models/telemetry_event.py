from typing import TYPE_CHECKING

from sqlalchemy import DateTime, func, Integer, String, ForeignKey, Boolean, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime

from app.db.base import Base
if TYPE_CHECKING:
    from app.models.device import Device


class TelemetryEvent(Base):
    __tablename__ = "telemetry_events"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    device_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("devices.id",
                   ondelete="CASCADE"),
        nullable=False,
        )
    metric_name: Mapped[str] = mapped_column(String(255), nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_anomaly: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    anomaly_score: Mapped[float] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    
    device: Mapped["Device"] = relationship(
        back_populates="telemetry_events"
    )
    
    