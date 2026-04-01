from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.core.config import settings

# Setup mail config safely
if settings.MAIL_USERNAME and settings.MAIL_PASSWORD and settings.MAIL_FROM:
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_STARTTLS=False,
        MAIL_SSL_TLS=True,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True
    )
    fast_mail = FastMail(conf)
else:
    fast_mail = None

async def send_verification_email(email: str, token: str):
    if not fast_mail:
        print(f"\n[MOCK EMAIL] To: {email} | Verification Token: {token}\n")
        return
        
    html = f"""
    <h2>Verify your University Portal Account</h2>
    <p>Please use the following OTP token to verify your account:</p>
    <h1>{token}</h1>
    """
    
    message = MessageSchema(
        subject="Account Verification - Campus Event System",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )
    
    try:
        await fast_mail.send_message(message)
        print(f"Live Email sent successfully to {email}")
    except Exception as e:
        print(f"Error sending email: {e}")
