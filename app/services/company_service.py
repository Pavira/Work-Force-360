import os
from uuid import uuid4
from sqlalchemy.orm import Session, selectinload
from fastapi import HTTPException, status

from app.models.company_models import (
    CompanyModel,
    CompanyAddressModel,
    CompanyDocumentModel,
)
from app.schemas.company_schema import (
    CompanyAddressCreateSchema,
    CompanyDocumentCreateSchema,
    CompanyInfoSchema,
    CompanyProfileUpdateSchema,
    ContactInfoSchema,
    DocumentInfoSchema,
)


# -----------------------Company profile exist or not Service ----------------------- #
def company_profile_exist_service(
    firebase_uid: str,
    db: Session,
) -> CompanyModel | None:

    return (
        db.query(CompanyModel).filter(CompanyModel.firebase_uid == firebase_uid).first()
    )


# -----------------------End Company profile exist or not Service ----------------------- #


# -----------------------Get Company Profile Service ----------------------- #
def get_company_profile_service(
    firebase_uid: str,
    db: Session,
) -> dict:

    company = (
        db.query(CompanyModel)
        .options(
            selectinload(CompanyModel.addresses),
            selectinload(CompanyModel.documents),
        )
        .filter(CompanyModel.firebase_uid == firebase_uid)
        .first()
    )

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company profile not found",
        )

    # Extract profile image from documents
    profile_image = None
    other_documents = []

    for doc in company.documents:
        if doc.document_type == "profile_image":
            profile_image = doc.document_url
        # else:
        #     other_documents.append(
        #         {
        #             "id": doc.id,
        #             "document_type": doc.document_type,
        #             "document_url": doc.document_url,
        #         }
        #     )

    return {
        "id": company.id,
        "firebase_uid": company.firebase_uid,
        "company_name": company.company_name,
        "industry_id": company.industry_id,
        "industry_name": company.industry_name,
        "gst_number": company.gst_number,
        "auth_phone": company.auth_phone,
        "contact_person_name": company.contact_person_name,
        "contact_phone": company.contact_phone,
        "contact_email": company.contact_email,
        "logo_url": company.logo_url,
        "status": company.status,
        "is_verified": company.is_verified,
        "is_active": company.is_active,
        "profile_image": profile_image,
        "addresses": [
            {
                "id": addr.id,
                "address": addr.address,
                "unit_name": addr.unit_name,
                "city": addr.city,
                "state": addr.state,
                "pincode": addr.pincode,
            }
            for addr in company.addresses
        ],
        "documents": other_documents,
        "created_at": company.created_at,
        "updated_at": company.updated_at,
    }


# -----------------------End Get Company Profile Service ----------------------- #


# -----------------------Create Company Profile Service----------------------- #
def create_company_profile_service(
    company: CompanyInfoSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:
        # Validation 1 - Prevent duplicate registration for same firebase_uid
        company_db = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )

        company_db = CompanyModel(
            firebase_uid=firebase_uid,
            company_name=company.companyName,
            industry_name=company.industryName,
            industry_id=company.industryId,
            gst_number=company.gstNo,
            auth_phone=company.authPhone,
        )
        db.add(company_db)
        db.flush()
        for addr in company.addresses:
            db.add(
                CompanyAddressModel(
                    company_id=company_db.id,
                    address=addr.address,
                    unit_name=addr.unitName,
                    city=addr.city,
                    state=addr.state,
                    pincode=addr.pincode,
                )
            )

        return company_db

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database transaction failed",
        )


# -----------------------End Create Company Profile Service----------------------- #


# -----------------------Update Contact Info Service----------------------- #
def update_contact_info_service(
    contact_info: ContactInfoSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:
        company_profile = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )

        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )

        # Check email uniqueness across other companies
        if contact_info.contactEmail:
            email_exists = (
                db.query(CompanyModel)
                .filter(
                    CompanyModel.contact_email == contact_info.contactEmail,
                    CompanyModel.firebase_uid != firebase_uid,
                )
                .first()
            )
            if email_exists:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered with another company",
                )

        # Update fields (industry standard)
        company_profile.contact_person_name = contact_info.contactPersonName
        company_profile.contact_phone = contact_info.contactPersonPhone
        company_profile.contact_email = contact_info.contactEmail

        db.flush()
        return company_profile
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating contact info",
        )


# -----------------------End Update Contact Info Service----------------------- #


# -----------------------Update Document Service----------------------- #
def update_document_info_service(
    contact_info: DocumentInfoSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:
        company_profile = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )
        if not company_profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )

        # Update contact info
        company_profile.logo_url = contact_info.logoUrl
        for doc in contact_info.documents:
            db.add(
                CompanyDocumentModel(
                    company_id=company_profile.id,
                    document_type=doc.documentType,
                    document_url=doc.documentUrl,
                )
            )

        db.add(company_profile)
        db.flush()
        return company_profile

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating contact info",
        )


# -----------------------End Update Document Service----------------------- #


# -----------------------Update Company Profile Service----------------------- #
def update_company_profile_service(
    update: CompanyProfileUpdateSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:

        company = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )

        data = update.model_dump(exclude_unset=True)

        # Simple field updates
        if "companyName" in data:
            company.company_name = data["companyName"]

        if "industryType" in data:
            company.industry = data["industryType"]

        if "gstNo" in data:
            company.gst_number = data["gstNo"]

        # Address update (replace strategy)
        if "addresses" in data:
            db.query(CompanyAddressModel).filter(
                CompanyAddressModel.company_id == company.id
            ).delete(synchronize_session=False)

            for addr in data["addresses"]:
                db.add(
                    CompanyAddressModel(
                        company_id=company.id,
                        address=addr["address"],
                        unit_name=addr["unitName"],
                        city=addr["city"],
                        state=addr["state"],
                        pincode=addr["pincode"],
                    )
                )
        # Contact Info update
        if "contactInfo" in data:
            ci = data["contactInfo"]

            if "contactPersonName" in ci:
                company.contact_person_name = ci["contactPersonName"]

            if "contactPersonPhone" in ci:
                company.contact_phone = ci["contactPersonPhone"]

            if "contactEmail" in ci:
                exists = (
                    db.query(CompanyModel)
                    .filter(
                        CompanyModel.contact_email == ci["contactEmail"],
                        CompanyModel.id != company.id,
                    )
                    .first()
                )
                if exists:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="Email already registered with another company",
                    )
                company.contact_email = ci["contactEmail"]

        # Document Info update
        if "documentInfo" in data:
            di = data["documentInfo"]

            if "logoUrl" in di:
                company.logo_url = di["logoUrl"]

            if "documents" in di:
                db.query(CompanyDocumentModel).filter(
                    CompanyDocumentModel.company_id == company.id
                ).delete(synchronize_session=False)

                for doc in di["documents"]:
                    db.add(
                        CompanyDocumentModel(
                            company_id=company.id,
                            document_type=doc.get("documentType"),
                            document_url=doc.get("documentUrl"),
                        )
                    )

        db.flush()
        return company

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating contact info",
        )


# -----------------------End Update Company Profile Service----------------------- #

# -----------------------Get Terms and Conditions Service----------------------- #
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="us-east-1",
)

objects = s3_client.list_objects_v2(Bucket="workforce360-terms", Prefix="company_docs/")

print(objects)

BUCKET_NAME = "workforce360-terms"
TERMS_KEY = "workforce_terms.html"  # latest pointer


def get_terms_and_conditions() -> str:
    try:
        response = s3_client.get_object(
            Bucket=BUCKET_NAME,
            Key=TERMS_KEY,
        )

        html_content = response["Body"].read().decode("utf-8")
        return html_content

    except ClientError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to fetch Terms and Conditions",
        )


# -----------------------End Get Terms and Conditions Service----------------------- #


# -----------------------Generate S3 Upload URL Service----------------------- #
def generate_upload_url_service(
    file_type: str,
    current_user,
) -> dict:
    try:
        allowed_types = ["png", "jpg", "jpeg", "pdf"]
        if file_type not in allowed_types:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type",
            )

        CONTENT_TYPES = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "pdf": "application/pdf",
        }

        key = f"company_docs/{current_user}/{uuid4()}.{file_type}"

        url = s3_client.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": "workforce360-terms",
                "Key": key,
                "ContentType": CONTENT_TYPES[file_type],
            },
            ExpiresIn=300,  # 5 minutes
        )

        return {
            "upload_url": url,
            "file_url": f"https://workforce360-terms.s3.amazonaws.com/{key}",
        }

    except HTTPException:
        raise
    except Exception as e:
        print("S3 ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error generating upload URL",
        )


# -----------------------End Generate S3 Upload URL Service----------------------- #


# -----------------------Save Document Service----------------------- #
def save_document_service(
    payload: CompanyDocumentCreateSchema,
    current_user: str,
    db: Session,
) -> CompanyDocumentModel:
    try:
        company = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == current_user)
            .first()
        )
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )

        document = CompanyDocumentModel(
            company_id=company.id,
            document_type=payload.documentType,
            document_url=payload.documentUrl,
        )
        db.add(document)
        db.flush()
        return document

    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving document",
        )


# -----------------------End Save Document Service----------------------- #


# -----------------------Get Document Service----------------------- #
def get_document_service(
    document_id: str,
    current_user: str,
    db: Session,
) -> str:
    document = (
        db.query(CompanyDocumentModel)
        .join(CompanyModel)
        .filter(
            CompanyDocumentModel.id == document_id,
            CompanyModel.firebase_uid == current_user,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    # Extract S3 key from URL
    s3_key = document.document_url.split(".com/")[1]

    presigned_url = s3_client.generate_presigned_url(
        ClientMethod="get_object",
        Params={
            "Bucket": "workforce360-terms",
            "Key": s3_key,
        },
        ExpiresIn=300,  # 5 minutes
    )

    return presigned_url


# -----------------------End Get Document Service----------------------- #


# -----------------------Delete Document Service----------------------- #
def delete_document_service(
    document_id: str,
    current_user: str,
    db: Session,
):
    document = (
        db.query(CompanyDocumentModel)
        .join(CompanyModel)
        .filter(
            CompanyDocumentModel.id == document_id,
            CompanyModel.firebase_uid == current_user,
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    # Extract S3 key
    s3_key = document.document_url.split(".com/")[1]

    # Delete from S3
    s3_client.delete_object(
        Bucket="workforce360-terms",
        Key=s3_key,
    )

    # Delete from DB
    db.delete(document)
    db.flush()


# -----------------------End Delete Document Service----------------------- #


# -----------------------Update Company Address Service----------------------- #
def update_company_address_service(
    address_id: str,
    new_address: CompanyAddressCreateSchema,
    db: Session,
) -> CompanyAddressModel:
    try:
        company_address = (
            db.query(CompanyAddressModel)
            .filter(CompanyAddressModel.id == address_id)
            .first()
        )

        if not company_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company address not found",
            )

        # Update fields
        company_address.address = new_address.address
        company_address.unit_name = new_address.unitName
        company_address.city = new_address.city
        company_address.state = new_address.state
        company_address.pincode = new_address.pincode

        db.flush()
        return company_address

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating company address",
        )


# -----------------------End Update Company Address Service----------------------- #


# -----------------------Add New Company Service----------------------- #
def add_new_company_service(
    new_address: CompanyAddressCreateSchema,
    firebase_uid: str,
    db: Session,
) -> CompanyModel:
    try:
        company = (
            db.query(CompanyModel)
            .filter(CompanyModel.firebase_uid == firebase_uid)
            .first()
        )

        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found",
            )

        new_company_address = CompanyAddressModel(
            company_id=company.id,
            address=new_address.address,
            unit_name=new_address.unitName,
            city=new_address.city,
            state=new_address.state,
            pincode=new_address.pincode,
        )
        db.add(new_company_address)
        db.flush()
        return company

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error adding new company address",
        )


# -----------------------End Add New Company Service----------------------- #


# -----------------------Delete Particular Company Address----------------------- #
def delete_company_address_service(
    address_id: str,
    db: Session,
) -> CompanyAddressModel:
    try:
        company_address = (
            db.query(CompanyAddressModel)
            .filter(CompanyAddressModel.id == address_id)
            .first()
        )

        if not company_address:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company address not found",
            )

        db.delete(company_address)
        db.flush()
        return company_address

    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting company address",
        )


# -----------------------End Delete Particular Company Address----------------------- #


# -----------------------Get All Company details Service----------------------- #
def get_all_company_details_service(
    db: Session,
) -> list[CompanyModel]:
    try:
        return db.query(CompanyModel).all()
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching all company details",
        )


# -----------------------End Get All Company details Service----------------------- #


# -----------------------Delete Company Details Service----------------------- #
def delete_company_profile_service(
    phone_number: str,
    db: Session,
) -> CompanyModel:
    try:
        company = (
            db.query(CompanyModel)
            .filter(CompanyModel.auth_phone == phone_number)
            .first()
        )

        db.query(CompanyAddressModel).filter(
            CompanyAddressModel.company_id == company.id
        ).delete()

        db.query(CompanyDocumentModel).filter(
            CompanyDocumentModel.company_id == company.id
        ).delete()

        db.delete(company)
        db.flush()

        return company
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting company details",
        )


# -----------------------End Delete Company Details Service----------------------- #


# -----------------------Get All Address details Service----------------------- #
def get_all_address_details_service(
    db: Session,
) -> list[CompanyAddressModel]:
    try:
        return db.query(CompanyAddressModel).all()
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching all address details",
        )


# -----------------------End Get All Address details Service----------------------- #


# -----------------------Get All Documents details Service----------------------- #
def get_all_documents_details_service(
    db: Session,
) -> list[CompanyDocumentModel]:
    try:
        return db.query(CompanyDocumentModel).all()
    except HTTPException:
        raise
    except Exception as e:
        print("DB ERROR 👉", e)  # or logger.exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching all document details",
        )


# -----------------------End Get All Documents details Service----------------------- #
