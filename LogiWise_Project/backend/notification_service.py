def send_sms(phone: str, message: str):
    print(f"📲 SMS SENT to {phone}: {message}")
    return True


def send_email(email: str, message: str):
    print(f"📧 EMAIL SENT to {email}: {message}")
    return True