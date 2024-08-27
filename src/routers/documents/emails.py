from email.message import Message
import os
from fastapi import UploadFile, File
from email import message_from_bytes
from email.policy import default

from lib.clients.openai import get_openai_chat_completion
from lib.clients.s3 import s3_client
from fastapi import APIRouter

router = APIRouter(prefix="/api/email_parser", tags=["email_parser"])


def get_email_body(msg: Message):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disposition = str(part.get("Content-Disposition"))

            # skip any text/plain (txt) attachments
            if ctype == "text/plain" and "attachment" not in disposition:
                return part.get_payload(decode=True)
    # not multipart - i.e. plain text, no attachments
    else:
        return msg.get_payload(decode=True)


@router.post("/process-email/")
async def process_email(email: UploadFile = File(...)):
    # Read the email content
    email_content = await email.read()

    # Parse the email
    msg = message_from_bytes(email_content, policy=default)

    body = get_email_body(msg)

    # Process attachments
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-Disposition") is None:
            continue

        filename = part.get_filename()
        if filename:
            # Save attachment to S3
            attachment_data = part.get_payload(decode=True)
            s3_client.put_object(
                Bucket=os.getenv("S3_BUCKET_NAME"),
                Key=f"attachments/{filename}",
                Body=attachment_data,
            )

    llm_response = await get_openai_chat_completion(
        system_message="You are a helpful assistant that processes email content.",
        user_message=f"Process this email body: {body}",
    )

    return {
        "message": "Email processed successfully",
        "attachments_saved": "Attachments saved to S3",
        "content": llm_response,
    }
