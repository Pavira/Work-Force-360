from fastapi import HTTPException, status
from geoalchemy2.shape import from_shape
from shapely.geometry import Point
from sqlalchemy.orm import Session

from app.models.industry_skill_models import (
    CategorySkillModel,
    IndustryTypeModel,
    SubCategorySkillModel,
)
from app.models.job_model import JobPostingModel
from app.schemas.job_schema import JobPostingSchema


def create_job_post_service(payload: JobPostingSchema, db: Session) -> dict:
    try:

        location = from_shape(
            Point(payload.longitude, payload.latitude),  # lng, lat order
            srid=4326,
        )

        job = JobPostingModel(
            skill_category_id=payload.skillCategoryId,
            sub_category_id=payload.subCategoryId,
            industry_type_id=payload.industryTypeId,
            tier=payload.tier,
            description=payload.description,
            location=location,
            work_address=payload.workAddress,
            nearby_landmark=payload.nearbyLandmark,
            scheduled_start_datetime=payload.scheduledStartDateTime,
            scheduled_end_datetime=payload.scheduledEndDateTime,
            scheduled_duration=payload.scheduledDuration,
            duration_type=payload.durationType,
            shift=payload.shift,
            workers=payload.workers,
            experience_required=payload.experienceRequired,
            wage=payload.wage,
            expected_total=payload.expectedTotal,
            name=payload.name,
            country_code=payload.countryCode,
            phone_number=payload.phoneNumber,
            email=payload.email,
            language_preference=payload.languagePreference,
            tool_provided=payload.toolProvided,
            tool_details=payload.toolDetails,
            special_instructions=payload.specialInstructions,
        )
        db.add(job)
        db.flush()
        return job

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating job post",
        )


# ------------------------END Job Post Service ------------------------


# ------------------------GET All Job Post Service ------------------------
def get_all_job_posts_service(db: Session) -> list:
    try:
        job_posts = (
            db.query(JobPostingModel).filter(JobPostingModel.is_active == True).all()
        )
        return job_posts
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving job posts",
        )


# ------------------------END GET All Job Post Service ------------------------


# ------------------------GET Job Post By ID Service ------------------------
def get_job_post_by_id_service(job_id: str, db: Session) -> JobPostingModel:
    try:
        job_post = (
            db.query(JobPostingModel)
            .filter(
                JobPostingModel.id == job_id,
                JobPostingModel.is_active == True,
            )
            .first()
        )
        if not job_post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Job post not found"
            )
        return job_post
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving job post",
        )


# ------------------------END GET Job Post By ID Service ------------------------
