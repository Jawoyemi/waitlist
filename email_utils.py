import os
import requests
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.api_key = os.getenv("SENDGRID_API_KEY")
        self.from_email = os.getenv("MAIL_FROM")
        self.url = "https://api.sendgrid.com/v3/mail/send"
        print(f"INFO: Initialized SendGrid Email Service with sender: {self.from_email}")

    def _send_email(self, to_email: str, subject: str, html_content: str):
        if not self.api_key:
            print("ERROR: SENDGRID_API_KEY is missing!")
            return

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "personalizations": [{"to": [{"email": to_email}]}],
            "from": {"email": self.from_email, "name": "UniBuy Team"},
            "subject": subject,
            "content": [{"type": "text/html", "value": html_content}]
        }

        try:
            response = requests.post(self.url, headers=headers, json=data)
            if response.status_code == 202:
                print(f"SUCCESS: Email sent to {to_email}")
            else:
                print(f"ERROR: SendGrid returned {response.status_code}: {response.text}")
        except Exception as e:
            print(f"ERROR: Failed to connect to SendGrid: {str(e)}")

    async def send_notification_email(self, user_email: str, admin_email: str):
        subject = "New Waitlist Signup!"
        html = f"<p>A new user has joined the waitlist: <strong>{user_email}</strong></p>"
        self._send_email(admin_email, subject, html)

    async def send_welcome_email(self, user_email: str):
        html_content = f"""
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
        self._send_email(user_email, "You're on the list! Welcome to UniBuy", html_content)
