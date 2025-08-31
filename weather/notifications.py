from twilio.rest import Client
from django.conf import settings
import firebase_admin
from firebase_admin import credentials, messaging
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Twilio SMS
def send_sms_alert(message):
    try:
        client = Client(settings.TWILIO_SID, settings.TWILIO_AUTH)
        msg = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE,
            to=settings.TEST_PHONE
        )
        logger.info(f"SMS sent successfully: {msg.sid}")
        return True
    except Exception as e:
        logger.error(f"SMS Error: {e}")
        return False

# Firebase Push - Initialize only once
try:
    cred = credentials.Certificate("D:/Users/admin/LJ_python_Project_sem4/DAIICT/coastal_alert_system/coastal-threats-firebase-adminsdk-fbsvc-e9ac4be4c9.json")
    firebase_admin.initialize_app(cred)
    logger.info("Firebase Admin SDK initialized successfully")
except Exception as e:
    logger.error(f"Firebase initialization error: {e}")

# List of valid FCM tokens (you should store these in your database instead)
VALID_FCM_TOKENS = [
    # Add your valid FCM tokens here
    # Example: "your_valid_fcm_token_here",
]

def send_push_alert(message, title="Alert"):
    """
    Send push notification to all registered devices.
    Returns True if at least one notification was sent successfully.
    """
    if not VALID_FCM_TOKENS:
        logger.warning("No FCM tokens registered. Skipping push notification.")
        return False
    
    success_count = 0
    total_count = len(VALID_FCM_TOKENS)
    
    for token in VALID_FCM_TOKENS:
        try:
            msg = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=message,
                ),
                token=token,
            )
            response = messaging.send(msg)
            logger.info(f"Push notification sent to token {token[:10]}...: {response}")
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to send push notification to token {token[:10]}...: {e}")
    
    logger.info(f"Push notifications: {success_count}/{total_count} successful")
    return success_count > 0

def add_fcm_token(token):
    """Add a new FCM token to the list of valid tokens"""
    if token not in VALID_FCM_TOKENS:
        VALID_FCM_TOKENS.append(token)
        logger.info(f"Added new FCM token: {token[:10]}...")
        return True
    return False

def remove_fcm_token(token):
    """Remove an FCM token from the list"""
    if token in VALID_FCM_TOKENS:
        VALID_FCM_TOKENS.remove(token)
        logger.info(f"Removed FCM token: {token[:10]}...")
        return True
    return False
