# utils.py

from mailersend import emails
from django.conf import settings


def get_template(status):
    if status == 'CF':
        return "7dnvo4d092xg5r86"
    elif status == 'CN':
        return "3yxj6ljw9d7gdo2r"
    elif status == 'EP':
        return "7dnvo4d092xg5r86"

def get_subject(status):
    if status == 'CF':
        return "Confirmación de Pedido"
    elif status == 'CN':
        return "Pedido Cancelado"
    elif status == 'EP':
        return "Pedido en Proceso"
    else:
        return "Actualización de Pedido"

def send_order_status_email(user_email, user_name, order_id, new_status):
    template = get_template(new_status)
    subject = get_subject(new_status)

    mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)
    mail_body = {}

    mail_from = {
        "name": "AntoJitos",
        "email": settings.DEFAULT_FROM_EMAIL,
    }

    recipients = [
        {
            "name": user_name,
            "email": user_email,
        }
    ]

    personalization = [
        {
            "email": user_email,
            "data": {
                "order_number": order_id,
                "order": {
                    "id": order_id,
                    "status": new_status
                }
            }
        }
    ]

    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    mailer.set_subject(subject, mail_body)
    mailer.set_template(template, mail_body)  # Reemplaza TEMPLATE_ID con el ID de tu plantilla
    mailer.set_advanced_personalization(personalization, mail_body)

    
    response = mailer.send(mail_body)



