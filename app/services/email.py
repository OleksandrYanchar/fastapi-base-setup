from abc import ABC, abstractmethod
from pathlib import Path

import jwt
from configs.auth import ALGORITHM, SECRET
from fastapi import Request
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from app.configs.emails import EMAIL_HOST_PASSWORD, EMAIL_HOST_USER, EMAIL_HOST_USERNAME
from app.models.users import Users


class EmailSender(ABC):
    def __init__(self):
        self.config = ConnectionConfig(
            MAIL_USERNAME=EMAIL_HOST_USERNAME,
            MAIL_PASSWORD=EMAIL_HOST_PASSWORD,
            MAIL_FROM=EMAIL_HOST_USER,
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )

    async def load_template(self, template_name: str) -> str:
        template_path = Path(__file__).parent.parent / f"templates/{template_name}"
        with open(template_path, "r") as f:
            template = f.read()
        return template

    @abstractmethod
    async def prepare_email_data(
        self, user: Users, request: Request, template: str
    ) -> str:
        pass

    async def send_email(self, user: Users, request: Request, template_name: str):
        base_template = await self.load_template(template_name)

        # Use the user object directly
        prepared_template = await self.prepare_email_data(user, request, base_template)
        message = MessageSchema(
            subject=self.subject,
            recipients=[user.email],
            body=prepared_template,
            subtype="html",
        )
        fm = FastMail(self.config)
        await fm.send_message(message)


class VerificationEmailSender(EmailSender):

    template_name = "send-verification.html"
    subject = "Verify Your Email Address"

    async def prepare_email_data(
        self, user: Users, request: Request, template: str
    ) -> str:
        token_data = {
            "user_id": str(user.id),
            "username": user.username,
        }
        token = jwt.encode(token_data, SECRET, algorithm=ALGORITHM)

        domain = str(request.base_url).rstrip("/")
        verification_path = "/users/auth/verification"
        url = f"{domain}{verification_path}?token={token}"

        prepared_template = template.replace('href="url"', f'href="{url}"')
        print(f"Verification URL: {url}")  # Debugging purposes
        return prepared_template


# Instantiate the email sender
verify_email_sender = VerificationEmailSender()
