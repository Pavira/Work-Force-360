from geoalchemy2 import Geography
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Text,
    Boolean,
    func,
    text,
    ForeignKey,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class JobPostingModel(Base):
    __tablename__ = "job_postings"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )

    # ---- References ----
    skill_category_id = Column(
        UUID(as_uuid=True), ForeignKey("skill_categories.id"), nullable=False
    )
    sub_category_id = Column(
        UUID(as_uuid=True), ForeignKey("sub_categories.id"), nullable=True
    )
    industry_type_id = Column(
        UUID(as_uuid=True), ForeignKey("industry_types.id"), nullable=True
    )

    tier = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)

    # ---- Location ----
    location = Column(Geography("POINT", 4326), nullable=False)
    work_address = Column(Text, nullable=True)
    nearby_landmark = Column(Text, nullable=True)

    # ---- Schedule ----
    scheduled_start_datetime = Column(DateTime(timezone=True), nullable=True)
    scheduled_end_datetime = Column(DateTime(timezone=True), nullable=True)
    scheduled_duration = Column(String, nullable=True)
    duration_type = Column(String, nullable=True)
    shift = Column(String, nullable=True)

    # ---- Actual Execution ----
    actual_start_at = Column(DateTime(timezone=True), nullable=True)
    actual_end_at = Column(DateTime(timezone=True), nullable=True)

    # ---- Workforce ----
    workers = Column(Integer, nullable=False)
    experience_required = Column(String, nullable=True)

    # ---- Payment ----
    wage = Column(Integer, nullable=False)
    expected_total = Column(Integer, nullable=False)

    # ---- Contact ----
    name = Column(String, nullable=True)
    country_code = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)

    # ---- Rules ----
    language_preference = Column(String, nullable=True)
    tool_provided = Column(Boolean, nullable=False)
    tool_details = Column(Text, nullable=True)
    special_instructions = Column(Text, nullable=True)

    # ---- Status ----
    status = Column(String, nullable=False)
    is_active = Column(Boolean, server_default=text("true"))

    # ---- Timestamps ----
    posted_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    assigned_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    cancelled_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    __table_args__ = (
        Index("idx_job_status", "status"),
        Index("idx_job_scheduled_start", "scheduled_start_datetime"),
    )
