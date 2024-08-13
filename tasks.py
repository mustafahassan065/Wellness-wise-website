from celery import shared_task
from .models import ChatMessage, ChatSession,User

@shared_task
def save_chat_message(session_id, user_id, message):
    try:
        session = ChatSession.objects.get(id=session_id)
        user = User.objects.get(id=user_id)
        ChatMessage.objects.create(chat_session=session, user=user, message_detail=message)
    except Exception as e:
        print(f"Error saving message: {e}")

@shared_task
def mark_message_as_read(message_id):
    try:
        message = ChatMessage.objects.get(id=message_id)
        message.read = True
        message.save()
    except Exception as e:
        print(f"Error marking message as read: {e}")
