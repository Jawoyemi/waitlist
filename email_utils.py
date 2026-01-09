import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from typing import List
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
            MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
            MAIL_FROM=os.getenv("MAIL_FROM"),
            MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
            MAIL_SERVER=os.getenv("MAIL_SERVER"),
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True
        )
        self.fastmail = FastMail(self.conf)

    async def send_notification_email(self, user_email: str, admin_email: str):
        try:
            message = MessageSchema(
                subject="New Waitlist Signup!",
                recipients=[admin_email],
                body=f"A new user has joined the waitlist: {user_email}",
                subtype=MessageType.html
            )
            await self.fastmail.send_message(message)
            print(f"SUCCESS: Admin notification sent for {user_email}")
        except Exception as e:
            print(f"ERROR: Failed to send admin notification: {str(e)}")

    async def send_welcome_email(self, user_email: str):
        html_content = """
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #eee; border-radius: 10px;">
                    <h2 style="color: #2c3e50; text-align: center;">Welcome to the UniBuy Waitlist! 🚀</h2>
                    <p>Hey there,</p>
                    <p>Thanks for joining the list! We're super excited to have you on board.</p>
                    
                    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p style="margin: 0; font-weight: 500;">
                            We're building <strong>UniBuy</strong> — A safe marketplace exclusively for <strong>UNIPORT & RSU students</strong>.
                        </p>
                        <p style="margin: 10px 0 0 0;">
                            You'll be able to buy and sell textbooks, gadgets, and services with verified peers on campus. No more sketchiness, just safe student-to-student commerce.
                        </p>
                    </div>

                    <p>We're just getting started, and since you're on the waitlist, you'll get <strong>early access</strong> as soon as we launch.</p>
                    
                    <p style="text-align: center; margin: 30px 0;">
                        <a href="https://x.com/UniBuy_1" style="background-color: #000; color: #fff; padding: 12px 25px; text-decoration: none; border-radius: 25px; font-weight: bold;">Follow us on X for updates</a>
                    </p>
                    
                    <p>Stay tuned!</p>
                    <p>— The UniBuy Team</p>
                </div>
            </body>
        </html>
        """
        
        try:
            message = MessageSchema(
                subject="You're on the list! Welcome to UniBuy",
                recipients=[user_email],
                body=html_content,
                subtype=MessageType.html
            )
            await self.fastmail.send_message(message)
            print(f"SUCCESS: Welcome email sent to {user_email}")
        except Exception as e:
            print(f"ERROR: Failed to send welcome email to {user_email}: {str(e)}")
