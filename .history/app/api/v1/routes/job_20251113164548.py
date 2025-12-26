from app.utils.response import custom_response
from fastapi import APIRouter, status, Path


router = APIRouter()


# ------------------------# Get job posting ------------------------
@router.post("/get_job_postings/{companyId}", status_code=status.HTTP_200_CREATED)
async def get_job_postings(
    companyId: int = Path(
        ..., description="The ID of the job to retrieve postings for a company"
    )
):
    """
    Retrieve job postings by company ID.
    """
    # Dummy data for demonstration purposes
    dummy_user = {
        "success": True,
        "message": "Job postings fetched successfully",
        "data": [
            {
                "jobId": "JOB_123456",
                "title": "Electrician",
                "subCategory": "House Wiring",
                "tier": 2,
                "companyId": "COMP_001",
                "companyName": "BrightFix Electricals",
                "companyLogoUrl": "https://storage.googleapis.com/.../logo.png",
                "createdBy": "USR_567889",
                "createdAt": "2025-11-10T15:30:00Z",
                "status": "searching",
                "wage": 250.0,
                "rateType": "hourly",
                "startDate": "2025-11-12",
                "startTime": "10:00 AM",
                "endDate": "2025-11-12",
                "endTime": "06:00 PM",
                "startTimestamp": "2025-11-12T10:00:00Z",
                "endTimestamp": "2025-11-12T18:00:00Z",
                "assignedWorker": None,
                "ratingByCompany": None,
                "ratingByWorker": None,
            },
            {
                "jobId": "JOB_7891011",
                "title": "Plumber",
                "subCategory": "Tap Fixing",
                "tier": 1,
                "companyId": "COMP_001",
                "companyName": "BrightFix Electricals",
                "companyLogoUrl": "https://storage.googleapis.com/.../logo.png",
                "createdBy": "USR_567889",
                "createdAt": "2025-11-09T13:20:00Z",
                "status": "assigned",
                "wage": 180.0,
                "rateType": "hourly",
                "startDate": "2025-11-13",
                "startTime": "02:00 PM",
                "endDate": "2025-11-13",
                "endTime": "06:00 PM",
                "startTimestamp": "2025-11-13T14:00:00Z",
                "endTimestamp": "2025-11-13T18:00:00Z",
                "assignedWorker": {
                    "workerId": "WORK_0091",
                    "name": "Arun Kumar",
                    "photoUrl": "https://storage.googleapis.com/.../arun.jpg",
                    "phone": "+919876543210",
                    "rating": 4.6,
                },
                "ratingByCompany": 4.8,
                "ratingByWorker": None,
            },
        ],
    }

    if companyId != 1:
        return custom_response(
            success=False,
            message=f"No job postings found for this company Id {companyId}.",
            data={},
            code=status.HTTP_404_NOT_FOUND,
        )
    return custom_response(
        success=True,
        message=f"Company Id {companyId} job postings retrieved successfully.",
        data=dummy_user,
        code=status.HTTP_200_OK,
    )


# ------------------------# Get job Details ------------------------
@router.post("/get_job_detail/{jobId}", status_code=status.HTTP_200_CREATED)
async def get_job_postings(
    jobId: int = Path(
        ..., description="The ID of the job to retrieve details for a company"
    )
):
    """
    Retrieve job Details by job ID.
    """
    # Dummy data for demonstration purposes
    dummy_user = {
        "success": True,
        "message": "Job details retrieved successfully",
        "data": {
            "jobId": "JOB_123456789",
            "role": "Electrician",
            "subCategory": "House Wiring",
            "tier": 2,
            "companyId": "COMP_001",
            "companyName": "BrightFix Electricals",
            "companyLogoUrl": "https://firebasestorage.googleapis.com/v0/b/app-bucket/o/company_logo.png",
            "createdBy": "USR_56789",
            "status": "confirmed",
            "wage": 250.0,
            "rateType": "hourly",
            "startDate": "2025-11-12",
            "startTime": "10:00 AM",
            "endDate": "2025-11-12",
            "endTime": "06:00 PM",
            "createdAt": "2025-11-10T15:30:00Z",
            "autoAssigned": False,
            "penalty": None,
            "assignedWorker": {
                "workerId": "WORK_00123",
                "name": "Arun Kumar",
                "photoUrl": "https://firebasestorage.googleapis.com/v0/b/app-bucket/o/workers/arun.jpg",
                "phone": "+919876543210",
                "rating": 4.7,
            },
            "timestamps": {
                "startTimestamp": "2025-11-12T10:00:00Z",
                "endTimestamp": "2025-11-12T18:00:00Z",
                "startedAt": "2025-11-12T10:02:13Z",
                "completedAt": None,
                "cancelledAt": None,
            },
            "ratingByCompany": 4.8,
            "ratingByWorker": 4.5,
            "paymentSummary": {
                "expectedHours": 8,
                "expectedEarnings": 2000,
                "actualHoursWorked": 0,
                "finalPayment": 0,
            },
        },
    }

    if jobId != 1:
        return custom_response(
            success=False,
            message=f"No job details found for this job Id {jobId}.",
            data={},
            code=status.HTTP_404_NOT_FOUND,
        )
    return custom_response(
        success=True,
        message=f"Job Id {jobId} details retrieved successfully.",
        data=dummy_user,
        code=status.HTTP_200_OK,
    )
