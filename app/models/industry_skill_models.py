from uuid import uuid4
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Boolean,
    DateTime,
    UniqueConstraint,
    text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.base import Base


class IndustryTypeModel(Base):
    __tablename__ = "industry_types"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    name = Column(String(150), nullable=False, unique=True)
    # description = Column(String(255), nullable=True)

    is_active = Column(Boolean, server_default=text("true"))
    # is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class CategorySkillModel(Base):
    __tablename__ = "category_skills"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    industry_type_id = Column(
        UUID(as_uuid=True),
        ForeignKey("industry_types.id", ondelete="RESTRICT"),
        nullable=False,
    )

    name = Column(String(150), nullable=False)
    # description = Column(String(255), nullable=True)

    is_active = Column(Boolean, server_default=text("true"))
    # is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Same category name can exist in different industries, but not twice inside the same industry.
    __table_args__ = (
        UniqueConstraint(
            "industry_type_id", "name", name="uq_category_skill_industry_name"
        ),
    )


class SubCategorySkillModel(Base):
    __tablename__ = "sub_category_skills"

    id = Column(
        UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()")
    )
    category_skill_id = Column(
        UUID(as_uuid=True),
        ForeignKey("category_skills.id", ondelete="RESTRICT"),
        nullable=False,
    )

    name = Column(String(150), nullable=False)
    # description = Column(String(255), nullable=True)

    is_active = Column(Boolean, server_default=text("true"))
    # is_deleted = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "category_skill_id", "name", name="uq_sub_category_skill_category_name"
        ),
    )
