from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from .models import Email, EmailVerificationEvent

EMAIL_HOST_USER = settings.EMAIL_HOST_USER

def verify_email(email):
    qs = Email.objects.filter(email=email, active=False)
    return qs.exists()

def get_verification_email_msg(verification_instance, as_html=False):
    if not isinstance(verification_instance, EmailVerificationEvent):
        return None
    verify_link =  verification_instance.get_link()
    if as_html:
        return f"<h1>Verify your email with the following</h1><p><a href='{verify_link}'>{verify_link}</a></p>"
    return f"Verify your email with the following:\n{verify_link}"


def start_verification_event(email):
    email_obj, created = Email.objects.get_or_create(email=email)
    obj = EmailVerificationEvent.objects.create(
        parent=email_obj,
        email=email
    )
    sent = send_verification_email(obj.id)
    return obj, sent

# celery task -> background task
def send_verification_email(verify_obj_id,):
    verify_obj = EmailVerificationEvent.objects.get(id=verify_obj_id)
    email = verify_obj.email
    subject = "Verify your email"
    text_msg = get_verification_email_msg(verify_obj, as_html=False)
    text_html = get_verification_email_msg(verify_obj, as_html=True)
    from_user_email_addr = EMAIL_HOST_USER
    to_user_email = email
    # send an verification email
    return send_mail(
        subject,
        text_msg,
        from_user_email_addr,
        [to_user_email],
        fail_silently=False,
        html_message=text_html
    )


def verify_token(token, max_attempts=5):
    qs = EmailVerificationEvent.objects.filter(token=token)
    if not qs.exists() and not qs.count() == 1:
        return False, "Invalid token", None
    """
    Has token
    """
    has_email_expired = qs.filter(expired=True)
    if has_email_expired.exists():
        """ token exipred"""
        return False, "Token expired, try again.", None
    """
    Has token, not expired
    """
    max_attempts_reached = qs.filter(attempts__gte=max_attempts)
    if max_attempts_reached.exists():
        """ update max attempts + 1"""
        # max_tempts_reached.update()
        return False, "Token expired, used too many times", None
    """Token valid"""
    """ update attempts, expire token if attempts > max"""
    obj = qs.first()
    obj.attempts += 1
    obj.last_attempt_at = timezone.now()
    if obj.attempts > max_attempts:
        """invalidation process"""
        obj.expired = True
        obj.expired_at = timezone.now()
    obj.save()
    email_obj = obj.parent # Email.objects.get()
    return True, "Welcome", email_obj



'''
Esta funcion se usa para mandar mails

import base64
import copy
import logging
import threading

from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GmailBackend(BaseEmailBackend):
    """
    Django email backend for sending with Google Workspace
    """
    def __init__(self, fail_silently=False, **kwargs):
        self.fail_silently = fail_silently
        self._lock = threading.RLock()
        service_account_key = settings.GMAIL_SERVICE_KEY
        # base_credentials used to build user specific credentials in send method
        self.base_credentials = service_account.Credentials.from_service_account_info(
            service_account_key,
            scopes=['https://www.googleapis.com/auth/gmail.send']
        )

    def open(self):
        """ retained for legacy code compaitibility """
        return True
    
    def close(self):
        """ retained for legacy code compaitibility """
        pass

    def send_messages(self, email_messages, thread=False):
        """
        Sends one or more EmailMessage objects and returns the number of email
        messages sent.
        """
        if not email_messages:
            return 0
        with self._lock:
            num_sent = 0
            for message in email_messages:
                sent = self._send(message)
                if sent:
                    num_sent += 1
        return num_sent

    def _send(self, email_message):
        """
        A helper method that does the actual sending.
        """
        if not email_message.recipients():
            return False
        try:
            # sanitize addresses
            sanitized_message = self.sanitize_addresses(email_message)
            message = sanitized_message.message()
            # Gmail api send() requires JSON format base64 string - convert .message() before sending
            raw = {"raw": base64.urlsafe_b64encode(message.as_bytes(linesep="\r\n")).decode("utf-8")}
            # Set delegated credentials according to the sender email address
            delegated_credentials = self.base_credentials.with_subject(email_message.from_email)
            service = build("gmail", "v1", credentials=delegated_credentials )
            # Send email
            service.users().messages().send(userId='me', body=raw).execute()
        except HttpError as e:
            logging.error(
                f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}"
            )
            if not self.fail_silently:
                raise
            return False
        return True
    
    def sanitize_addresses(self, email_message):
        """ 
        Make a copy of email message (email_message passed by reference), sanitize addresses 
        Ensure that email addresses are properly formatted & without potentially harmful characters
        """
        message_copy = copy.copy(email_message)
        encoding = email_message.encoding or getattr(settings, 'DEFAULT_CHARSET', 'utf-8')
        message_copy.from_email = sanitize_address(email_message.from_email, encoding)
        for field in ['to', 'cc', 'bcc', 'reply_to']:
            setattr(message_copy, field, [sanitize_address(addr, encoding) for addr in getattr(email_message, field)])
        return message_copy

contantes de configuracion de la cuenta de gmail
        EMAIL_BACKEND = "core.mail.backends.GmailBackend"
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER = 'someone@somewhere.com'
GMAIL_SERVICE_KEY = { ... }

'''