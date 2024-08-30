import random
import string
from notifications.email import Email
from authentication.models import ForgetPassword

def message(subject: str, extra: str) -> str:
    if subject.lower() == "email verification":
        message = f"Your email verification is {extra}"
        email_template = "email/email_verification.html"
    elif subject.lower() == "reset password":
        message = f"Your password reset OTP is {extra}"
        email_template = "email/reset_password.html"
    else:
        email_template = ""
        message = ""
    
    return message, email_template

def generate_otp(user: object) -> str:
    otp = "".join(random.choices(string.digits, k=6))
    ForgetPassword.objects.update_or_create(user=user, otp=otp)
    return otp

def check_otp(user: object, otp: str = None) -> bool:
    otp_ = ForgetPassword.objects.filter(user=user, otp=otp)
    return otp_.exists()

def send_otp(user: object, email: str, subject: str) -> bool:
    otp = generate_otp(user)
    extra = {"otp_code": otp, "user": user}
    send_email(email, subject, extra)

def send_email(email: str, subject: str, extra: dict = None):
    message_, template_ = message(subject, extra)

    # data = None
    # if extra:
    #     data = extra

    data = extra if extra else {}

    Email(
        subject=subject,
        receiver=email,
        plain_message=f"{message_}",
        template=template_,
        data=data
    ).send()
    return True

