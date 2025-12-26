from app.utils.response import custom_response
from fastapi import APIRouter, status, Path


router = APIRouter()


# ------------------------# Get job posting by companyId ------------------------
@router.get("/get_job_postings/{companyId}", status_code=status.HTTP_200_OK)
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


# ------------------------# Get job Details By jobId ------------------------
@router.get("/get_job_detail/{jobId}", status_code=status.HTTP_200_OK)
async def get_job_details(
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


# ------------------------# Get job By userId ------------------------
@router.get("/get_jobs/{userId}", status_code=status.HTTP_200_OK)
async def get_job_by_userId(
    userId: int = Path(..., description="Retrieve job Details by user ID")
):
    """
    Retrieve job Details by user ID.
    """
    # Dummy data for demonstration purposes
    dummy_user = {
        "success": True,
        "message": "Jobs fetched successfully",
        "data": {
            "upcomingJobs": [
                {
                    "jobId": "JOB_001",
                    "title": "Electrician",
                    "subCategory": "House Wiring",
                    "tier": 2,
                    "companyId": "COMP_001",
                    "companyName": "BrightFix Electricals",
                    "companyLogoUrl": "https://storage.googleapis.com/.../logo.png",
                    "status": "assigned",
                    "wage": 250,
                    "startDate": "2025-11-20",
                    "startTime": "10:00 AM",
                    "endDate": "2025-11-20",
                    "endTime": "06:00 PM",
                    "startTimestamp": "2025-11-20T10:00:00Z",
                    "endTimestamp": "2025-11-20T18:00:00Z",
                    "assignedWorker": {
                        "workerId": "WORK_109",
                        "name": "Arun Kumar",
                        "photoUrl": "https://storage.googleapis.com/.../arun.jpg",
                        "phone": "+919876543210",
                        "rating": 4.7,
                    },
                    "ratingByCompany": None,
                    "ratingByWorker": None,
                }
            ],
            "pastJobs": [
                {
                    "jobId": "JOB_002",
                    "title": "Carpenter",
                    "subCategory": "Furniture Fixing",
                    "tier": 1,
                    "companyId": "COMP_002",
                    "companyName": "UrbanFix Services",
                    "companyLogoUrl": "https://storage.googleapis.com/.../urbanfix.png",
                    "status": "completed",
                    "wage": 200,
                    "startDate": "2025-11-10",
                    "startTime": "09:00 AM",
                    "endDate": "2025-11-10",
                    "endTime": "01:00 PM",
                    "startTimestamp": "2025-11-10T09:00:00Z",
                    "endTimestamp": "2025-11-10T13:00:00Z",
                    "startedAt": "2025-11-10T09:05:00Z",
                    "completedAt": "2025-11-10T13:02:00Z",
                    "ratingByCompany": 4.8,
                    "ratingByWorker": 4.5,
                    "paymentSummary": {"totalHours": 4, "totalEarnings": 800},
                }
            ],
        },
    }

    if userId != 1:
        return custom_response(
            success=False,
            message=f"No job details found for this user Id {userId}.",
            data={},
            code=status.HTTP_404_NOT_FOUND,
        )
    return custom_response(
        success=True,
        message=f"User Id {userId} job details retrieved successfully.",
        data=dummy_user,
        code=status.HTTP_200_OK,
    )


# ------------------------# Get work details By jobId ------------------------
@router.get("/get_work_details/{jobId}", status_code=status.HTTP_200_OK)
async def get_work_details(
    jobId: int = Path(..., description="Retrieve job Details by job ID")
):
    """
    Retrieve job Details by Job ID.
    """
    # Dummy data for demonstration purposes
    dummy_user = {
        "success": True,
        "message": "Work details fetched successfully",
        "data": {
            "jobId": "JOB_123456",
            "title": "Electrician",
            "subCategory": "Wiring",
            "companyName": "BrightFix Electricals",
            "companyLogoUrl": "https://storage.googleapis.com/.../logo.png",
            "status": "ongoing",
            "wage": 250.0,
            "rateType": "hourly",
            "startDate": "2025-11-12",
            "startTime": "10:00 AM",
            "endDate": "2025-11-12",
            "endTime": "06:00 PM",
            "startTimestamp": "2025-11-12T10:00:00Z",
            "endTimestamp": "2025-11-12T18:00:00Z",
            "startedAt": "2025-11-12T10:03:21Z",
            "completedAt": None,
            "endedAt": None,
            "companyContact": {"name": "Prakash", "phone": "+919876543210"},
            "worker": {
                "workerId": "WORK_9911",
                "name": "Arun Kumar",
                "phone": "+918888888888",
            },
            "otpRequired": True,
            "otpLength": 4,
            "expectedEarnings": {"expectedHours": 8, "expectedAmount": 2000},
        },
    }

    if jobId != 1:
        return custom_response(
            success=False,
            message=f"No work details found for this job Id {jobId}.",
            data={},
            code=status.HTTP_404_NOT_FOUND,
        )
    return custom_response(
        success=True,
        message=f"Job Id {jobId} work details retrieved successfully.",
        data=dummy_user,
        code=status.HTTP_200_OK,
    )
