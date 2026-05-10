from fastapi import APIRouter
from pydantic import BaseModel
from notification_service import send_sms, send_email

router = APIRouter(prefix="/notify", tags=["Notification"])

class NotifyRequest(BaseModel):
    customer_name: str
    message: str
    channel: str  # sms | email


# demo müşteri verisi (sonra DB olur)
contacts = {
    "Ahmet Yılmaz": {
        "phone": "+905551112233",
        "email": "ahmet@example.com"
    }
}


@router.post("/customer")
def notify_customer(req: NotifyRequest):

    customer = contacts.get(req.customer_name)

    if not customer:
        return {"status": "error", "message": "Customer not found"}

    if req.channel == "sms":
        send_sms(customer["phone"], req.message)

    elif req.channel == "email":
        send_email(customer["email"], req.message)

    else:
        return {"status": "error", "message": "Invalid channel"}

    return {
        "status": "success",
        "sent_to": req.customer_name,
        "channel": req.channel
    }