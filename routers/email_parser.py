from email.message import Message
import os
from fastapi import FastAPI, UploadFile, File
from email import message_from_bytes
from email.policy import default
import boto3
from lib.clients.openai import client
from fastapi import APIRouter

app = FastAPI()

router = APIRouter(prefix="/api/email_parser", tags=["email_parser"])

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def get_email_body(msg: Message[str, str]):
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get("Content-Disposition"))

            # skip any text/plain (txt) attachments
            if ctype == "text/plain" and "attachment" not in cdispo:
                return part.get_payload(decode=True)
    # not multipart - i.e. plain text, no attachments
    else:
        return msg.get_payload(decode=True)


@app.post("/process-email/")
async def process_email(email: UploadFile = File(...)):
    # Read the email content
    email_content = await email.read()

    # Parse the email
    msg = message_from_bytes(email_content, policy=default)

    body = get_email_body(msg)
    # # Extract email body
    # if msg.is_multipart():
    #     body = ""
    #     for part in msg.walk():
    #         if part.get_content_type() == "text/plain":
    #             body = part.get_payload(decode=True).decode()
    #             break
    # else:
    #     body = msg.get_payload(decode=True).decode()

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
            s3.put_object(
                Bucket=os.getenv("S3_BUCKET_NAME"),
                Key=f"attachments/{filename}",
                Body=attachment_data,
            )

    # Pass email body to OpenAI
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that processes email content.",
            },
            {"role": "user", "content": f"Process this email body: {body}"},
        ],
    )

    content = response.choices[0].message.content

    return {
        "message": "Email processed successfully",
        "attachments_saved": "Attachments saved to S3",
        "content": content,
    }
