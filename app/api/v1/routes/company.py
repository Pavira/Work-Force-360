from uuid import UUID, uuid4
from fastapi import APIRouter, Request, Response, status, Depends
from sqlalchemy.orm import Session
from app.core.firebase_auth import get_current_user
from app.db.session import get_db
from app.core.limiter import limiter

from app.utils.response import custom_response
from app.schemas.company_schema import (
    CompanyAddressCreateSchema,
    CompanyBankDetailsSchema,
    CompanyDocumentCreateSchema,
    CompanyInfoSchema,
    CompanyProfileDetailsSchema,
    # CompanyProfileUpdateSchema,
    ContactInfoSchema,
    DocumentInfoSchema,
    UploadUrlRequest,
)
from app.services.company_service import (
    add_new_company_service,
    company_profile_exist_service,
    create_company_bank_details_service,
    create_company_profile_service,
    delete_company_address_service,
    delete_company_bank_details_service,
    delete_company_profile_service,
    delete_document_service,
    generate_upload_url_service,
    get_all_address_details_service,
    get_all_company_details_service,
    get_all_documents_details_service,
    get_company_documents_by_type_service,
    get_company_profile_service,
    get_document_service,
    get_terms_and_conditions,
    save_document_service,
    update_company_address_service,
    update_company_bank_details_service,
    update_company_profile_details_service,
    # update_company_profile_service,
    update_contact_info_service,
    update_document_info_service,
)


router = APIRouter()


# -----------------------Company exist or not------------------------ #
@router.get("/company_exists", status_code=status.HTTP_200_OK)
def company_exists(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Check if company profile exists (Firebase authenticated).
    """

    company = company_profile_exist_service(
        firebase_uid=current_user["uid"],
        db=db,
    )

    if not company:
        return custom_response(
            success=True,
            message="Company profile not found",
            data={"exists": False},
            code=status.HTTP_200_OK,
        )

    return custom_response(
        success=True,
        message="Company profile found",
        data={
            "exists": True,
            "id": company.id,
            "company_name": company.company_name,
            "status": company.status,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Company exist or not----------------------- #


# -----------------------Create Company Profile----------------------- #
@router.post(
    "/create_company_profile",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(
    "30/minute"
)  # Allow only 5 requests per minute per IP, ex - requests/minute - 10/second
def create_company_profile(
    request: Request,  # REQUIRED by SlowAPI
    company: CompanyInfoSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new company profile (Firebase authenticated) .
    """
    company_db = create_company_profile_service(
        company=company,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Company created successfully",
        data={
            "id": company_db.id,
            "company_name": company_db.company_name,
            "status": company_db.status,
        },
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Create Company Profile----------------------- #


# -----------------------Update Contact Person Info----------------------- #
@router.patch(
    "/update_contact_info",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(
    "30/minute"
)  # Allow only 5 requests per minute per IP, ex - requests/minute - 10/second
def update_contact_info(
    request: Request,  # REQUIRED by SlowAPI
    company: ContactInfoSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update contact person info for company profile (Firebase authenticated) .
    """
    company_db = update_contact_info_service(
        contact_info=company,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Contact info updated successfully",
        data={
            "contact_person_name": company_db.contact_person_name,
            # "company_name": company_db.company_person_name,
            # "status": company_db.status,
        },
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Update Contact Person Info----------------------- #


# -----------------------Update Document Info----------------------- #
@router.patch(
    "/update_document_info",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(
    "30/minute"
)  # Allow only 5 requests per minute per IP, ex - requests/minute - 10/second
def update_document_info(
    request: Request,  # REQUIRED by SlowAPI
    company: DocumentInfoSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update document info for company profile (Firebase authenticated) .
    """
    company_db = update_document_info_service(
        contact_info=company,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Document info updated successfully",
        data={
            # "id": company_db.id,
            # "company_name": company_db.company_person_name,
            # "status": company_db.status,
        },
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Update Document Info----------------------- #


# -----------------------Get Company Profile Route----------------------- #
@router.get(
    "/get_company_profile",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_company_profile(
    request: Request,  # REQUIRED by SlowAPI
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Get company profile (Firebase authenticated).
    """
    company_details = get_company_profile_service(
        firebase_uid=current_user["uid"], db=db
    )

    return custom_response(
        success=True,
        message="Company profile fetched successfully",
        data=company_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get Company Profile Route----------------------- #


# -----------------------Update Company Profile Route----------------------- #
# @router.patch(
#     "/update_company_profile",
#     status_code=status.HTTP_201_CREATED,
# )
# @limiter.limit("30/minute")
# def update_company_profile(
#     request: Request,  # REQUIRED by SlowAPI
#     company_profile: CompanyProfileUpdateSchema,
#     db: Session = Depends(get_db),
#     current_user: dict = Depends(get_current_user),
# ):
#     """
#     Update company profile (Firebase authenticated) .
#     """
#     company_db = update_company_profile_service(
#         update=company_profile,
#         firebase_uid=current_user["uid"],
#         db=db,
#     )

#     return custom_response(
#         success=True,
#         message="Company profile updated successfully",
#         data={
#             "id": company_db.id,
#             "company_name": company_db.company_name,
#             "status": company_db.status,
#         },
#         code=status.HTTP_201_CREATED,
#     )


# -----------------------End Update Company Profile Service----------------------- #
# -----------------------Fetch Terms and Conditions----------------------- #
@router.get(
    "/terms",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def fetch_terms_and_conditions(
    request: Request,  # REQUIRED by SlowAPI
):
    """
    Fetch latest Terms and Conditions
    """

    html = get_terms_and_conditions()
    return Response(content=html, media_type="text/html")


# -----------------------End Fetch Terms and Conditions----------------------- #


# -----------------------Generate S3 Upload URL----------------------- #


@router.put("/documents/upload-url")
@limiter.limit("30/minute")
def generate_upload_url(
    request: Request,  # REQUIRED by SlowAPI
    payload: UploadUrlRequest,
    current_user=Depends(get_current_user),
):

    urls = generate_upload_url_service(
        file_type=payload.file_type, current_user=current_user["uid"]
    )

    return custom_response(
        success=True,
        message="Upload URL generated successfully",
        data=urls,
        code=status.HTTP_200_OK,
    )


# -----------------------End Generate S3 Upload URL----------------------- #


# -----------------------Save Document----------------------- #
@router.post("/documents")
@limiter.limit("30/minute")
def save_document(
    request: Request,  # REQUIRED by SlowAPI
    payload: CompanyDocumentCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    document = save_document_service(
        payload=payload, current_user=current_user["uid"], db=db
    )

    return custom_response(
        success=True,
        message="Document saved successfully",
        data={"id": document.id, "document_type": document.document_type},
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Save Document----------------------- #


# -----------------------Get Document----------------------- #
@router.get("/documents/{document_id}")
@limiter.limit("30/minute")
def get_document(
    request: Request,  # REQUIRED by SlowAPI
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    url = get_document_service(
        document_id=document_id,
        current_user=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Document fetched successfully",
        data={"view_url": url},
        code=status.HTTP_200_OK,
    )


# -----------------------End Get Document----------------------- #


# -----------------------Delete Document----------------------- #
@router.delete("/documents/{document_id}")
@limiter.limit("30/minute")
def delete_document(
    request: Request,  # REQUIRED by SlowAPI
    document_id: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    delete_document_service(
        document_id=document_id,
        current_user=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Document deleted successfully",
        data={},
        code=status.HTTP_200_OK,
    )


# -----------------------End Delete Document----------------------- #


# -----------------------Update Company Address in profile----------------------- #
@router.patch("/update_company_address/{address_id}")
@limiter.limit("30/minute")
def update_company_address(
    request: Request,  # REQUIRED by SlowAPI
    address_id: UUID,
    new_address: CompanyAddressCreateSchema,
    db: Session = Depends(get_db),
):
    company_address = update_company_address_service(
        address_id=address_id,
        new_address=new_address,
        db=db,
    )

    return custom_response(
        success=True,
        message="Company address updated successfully",
        data={"company_address": company_address},
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Company Address----------------------- #


# -----------------------Add New Company Address----------------------- #
@router.post("/add_new_company_address")
@limiter.limit("30/minute")
def add_new_company_address(
    request: Request,  # REQUIRED by SlowAPI
    new_address: CompanyAddressCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    company_address = add_new_company_service(
        new_address=new_address,
        db=db,
        firebase_uid=current_user["uid"],
    )

    return custom_response(
        success=True,
        message="New company address added successfully",
        data={"company_address": company_address},
        code=status.HTTP_200_OK,
    )


# -----------------------End Add New Company Address----------------------- #


# -----------------------Delete Particular Company Address----------------------- #
@router.delete("/delete_company_address/{address_id}")
@limiter.limit("30/minute")
def delete_company_address(
    request: Request,  # REQUIRED by SlowAPI
    address_id: UUID,
    db: Session = Depends(get_db),
):
    company_address = delete_company_address_service(
        address_id=address_id,
        db=db,
    )

    return custom_response(
        success=True,
        message="Company address deleted successfully",
        data={"company_address": company_address},
        code=status.HTTP_200_OK,
    )


# -----------------------End Delete Particular Company Address----------------------- #


# -----------------------Get All Company Details----------------------- #
@router.get(
    "/all_company_details",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def get_all_company_details(
    request: Request,  # REQUIRED by SlowAPI
    db: Session = Depends(get_db),
):
    """
    Get all company details.
    """
    company_details = get_all_company_details_service(db=db)

    return custom_response(
        success=True,
        message="All company details fetched successfully",
        data=company_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get All Company Details----------------------- #


# -----------------------Delete company details----------------------- #
@router.delete(
    "/delete_company/{phone_number}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("10/minute")
def delete_company_details(
    request: Request,  # REQUIRED by SlowAPI
    phone_number: str,
    db: Session = Depends(get_db),
):
    """
    Delete company details.
    """
    company_details = delete_company_profile_service(phone_number=phone_number, db=db)

    return custom_response(
        success=True,
        message="Company details deleted successfully",
        data=company_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Delete company details----------------------- #


# -----------------------Get All Address Details----------------------- #
@router.get(
    "/all_address_details",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def get_all_address_details(
    request: Request,  # REQUIRED by SlowAPI
    db: Session = Depends(get_db),
):
    """
    Get all address details.
    """
    address_details = get_all_address_details_service(db=db)

    return custom_response(
        success=True,
        message="All address details fetched successfully",
        data=address_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get All Address Details----------------------- #


# -----------------------Get All Documents Details----------------------- #
@router.get(
    "/all_documents_details",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def get_all_documents_details(
    request: Request,  # REQUIRED by SlowAPI
    db: Session = Depends(get_db),
):
    """
    Get all documents details.
    """
    documents_details = get_all_documents_details_service(db=db)

    return custom_response(
        success=True,
        message="All documents details fetched successfully",
        data=documents_details,
        code=status.HTTP_200_OK,
    )


# -----------------------End Get All Documents Details----------------------- #


# -----------------------Update Company Profile Details----------------------- #
@router.patch(
    "/update_company_profile_details",
    status_code=status.HTTP_200_OK,
)
@limiter.limit(
    "30/minute"
)  # Allow only 5 requests per minute per IP, ex - requests/minute - 10/second
def update_company_profile_details(
    request: Request,  # REQUIRED by SlowAPI
    company_details: CompanyProfileDetailsSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update company profile details (Firebase authenticated) .
    """
    company_details = update_company_profile_details_service(
        company_details=company_details,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Company profile details updated successfully",
        data={
            "id": company_details.id,
            # "company_name": company_db.company_name,
            # "status": company_db.status,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Profile Details----------------------- #


# -----------------------Create Company Bank Details----------------------- #
@router.post(
    "/create_company_bank_details",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
def create_company_bank_details(
    request: Request,  # REQUIRED by SlowAPI
    bank_details: CompanyBankDetailsSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create company bank details (Firebase authenticated) .
    """
    bank_db = create_company_bank_details_service(
        bank_details=bank_details,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Company bank details created successfully",
        data={
            "id": bank_db.id,
        },
        code=status.HTTP_201_CREATED,
    )


# -----------------------End Create Company Bank Details----------------------- #


# -----------------------Update Company Bank Details----------------------- #
@router.patch(
    "/update_company_bank_details",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def update_company_bank_details(
    request: Request,  # REQUIRED by SlowAPI
    bank_details: CompanyBankDetailsSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update company bank details (Firebase authenticated) .
    """
    bank_db = update_company_bank_details_service(
        bank_details=bank_details,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Company bank details updated successfully",
        data={
            "id": bank_db.id,
        },
        code=status.HTTP_200_OK,
    )


# -----------------------End Update Company Bank Details----------------------- #


# -----------------------Delete Company Bank Details----------------------- #
@router.delete(
    "/delete_company_bank_details",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def delete_company_bank_details(
    request: Request,  # REQUIRED by SlowAPI
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete company bank details (Firebase authenticated) .
    """
    delete_status = delete_company_bank_details_service(
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Company bank details deleted successfully",
        data={"deleted": delete_status},
        code=status.HTTP_200_OK,
    )


# -----------------------End Delete Company Bank Details----------------------- #
# -----------------------Get Company Documents based on document type----------------------- #
@router.get(
    "/get_company_documents/{document_type}",
    status_code=status.HTTP_200_OK,
)
@limiter.limit("30/minute")
def get_company_documents(
    request: Request,  # REQUIRED by SlowAPI
    document_type: str,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Get company documents based on document type (Firebase authenticated) .
    """
    documents = get_company_documents_by_type_service(
        document_type=document_type,
        firebase_uid=current_user["uid"],
        db=db,
    )

    return custom_response(
        success=True,
        message="Company documents fetched successfully",
        data={"documents": documents},
        code=status.HTTP_200_OK,
    )
