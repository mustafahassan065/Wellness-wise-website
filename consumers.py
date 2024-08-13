from channels.generic.websocket import AsyncWebsocketConsumer
import json
from datetime import datetime
from my_app.models import ChatSession, ChatMessage
from channels.db import database_sync_to_async
import uuid
from .models import Profile
from django.db.models import Q
from .tasks import save_chat_message, mark_message_as_read

MESSAGE_MAX_LENGTH = 1000  # Adjusted to a reasonable value for actual message length

MESSAGE_ERROR_TYPE = {
    "MESSAGE_OUT_OF_LENGTH": 'MESSAGE_OUT_OF_LENGTH',
    "UN_AUTHENTICATED": 'UN_AUTHENTICATED',
    "INVALID_MESSAGE": 'INVALID_MESSAGE',
}

MESSAGE_TYPE = {
    "WENT_ONLINE": 'WENT_ONLINE',
    "WENT_OFFLINE": 'WENT_OFFLINE',
    "IS_TYPING": 'IS_TYPING',
    "NOT_TYPING": 'NOT_TYPING',
    "MESSAGE_COUNTER": 'MESSAGE_COUNTER',
    "OVERALL_MESSAGE_COUNTER": 'OVERALL_MESSAGE_COUNTER',
    "TEXT_MESSAGE": 'TEXT_MESSAGE',
    "MESSAGE_READ": 'MESSAGE_READ',
    "ALL_MESSAGE_READ": 'ALL_MESSAGE_READ',
    "ERROR_OCCURED": 'ERROR_OCCURED'
}

class PersonalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'personal__{self.room_name}'
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close(code=4001)

    async def disconnect(self, code):
        if self.user.is_authenticated:
            await self.set_offline()
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            msg_type = data.get('msg_type')
            user_id = data.get('user_id')

            if msg_type == MESSAGE_TYPE['WENT_ONLINE']:
                users_room_id = await self.set_online(user_id)
                for room_id in users_room_id:
                    await self.channel_layer.group_send(
                        f'personal__{room_id}',
                        {
                            'type': 'user_online',
                            'user_name': self.user.username
                        }
                    )
            elif msg_type == MESSAGE_TYPE['WENT_OFFLINE']:
                users_room_id = await self.set_offline(user_id)
                for room_id in users_room_id:
                    await self.channel_layer.group_send(
                        f'personal__{room_id}',
                        {
                            'type': 'user_offline',
                            'user_name': self.user.username
                        }
                    )
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'msg_type': MESSAGE_TYPE['ERROR_OCCURED'],
                'error_message': MESSAGE_ERROR_TYPE["INVALID_MESSAGE"],
            }))

    async def user_online(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['WENT_ONLINE'],
            'user_name': event['user_name']
        }))

    async def user_offline(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['WENT_OFFLINE'],
            'user_name': event['user_name']
        }))

    @database_sync_to_async
    def set_online(self, user_id):
        Profile.objects.filter(user__id=user_id).update(is_online=True)
        user_all_friends = ChatSession.objects.filter(Q(user1=self.user) | Q(user2=self.user))
        user_ids = [session.user2.id if self.user == session.user1 else session.user1.id for session in user_all_friends]
        return user_ids

    @database_sync_to_async
    def set_offline(self, user_id=None):
        Profile.objects.filter(user__id=user_id).update(is_online=False)
        user_all_friends = ChatSession.objects.filter(Q(user1=self.user) | Q(user2=self.user))
        user_ids = [session.user2.id if self.user == session.user1 else session.user1.id for session in user_all_friends]
        return user_ids


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = self.room_name
        self.user = self.scope['user']

        if self.user.is_authenticated:
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.accept()
            await self.send(text_data=json.dumps({
                "msg_type": MESSAGE_TYPE['ERROR_OCCURED'],
                "error_message": MESSAGE_ERROR_TYPE["UN_AUTHENTICATED"],
                "user": self.user.username,
            }))
            await self.close(code=4001)

    async def disconnect(self, code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message = data.get('message')
            msg_type = data.get('msg_type')

            if msg_type == MESSAGE_TYPE['TEXT_MESSAGE']:
                if len(message) <= MESSAGE_MAX_LENGTH:
                    msg_id = uuid.uuid4()

                    await self.channel_layer.group_send(
                        self.room_group_name,
                        {
                            'type': 'chat_message',
                            'message': message,
                            'user': self.user.username,
                            'msg_id': str(msg_id),
                        }
                    )

                    await save_chat_message(self.user.id, message)

                else:
                    await self.send(text_data=json.dumps({
                        'msg_type': MESSAGE_TYPE['ERROR_OCCURED'],
                        'error_message': MESSAGE_ERROR_TYPE["MESSAGE_OUT_OF_LENGTH"],
                        'message': message,
                        'user': self.user.username,
                        'timestamp': str(datetime.now()),
                    }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'msg_type': MESSAGE_TYPE['ERROR_OCCURED'],
                'error_message': MESSAGE_ERROR_TYPE["INVALID_MESSAGE"],
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['TEXT_MESSAGE'],
            'message': event['message'],
            'user': event['user'],
            'timestamp': str(datetime.now()),
            'msg_id': event["msg_id"]
        }))

    async def msg_as_read(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['MESSAGE_READ'],
            'msg_id': event['msg_id'],
            'user': event['user']
        }))

    async def all_msg_read(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['ALL_MESSAGE_READ'],
            'user': event['user']
        }))

    async def user_is_typing(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['IS_TYPING'],
            'user': event['user']
        }))

    async def user_not_typing(self, event):
        await self.send(text_data=json.dumps({
            'msg_type': MESSAGE_TYPE['NOT_TYPING'],
            'user': event['user']
        }))

    @database_sync_to_async
    def save_text_message(self, msg_id, message):
        session_id = self.room_name.split('__')[1]  # Extract session ID from room name
        session_inst = ChatSession.objects.select_related('user1', 'user2').get(id=session_id)
        message_json = {
            "msg": message,
            "read": False,
            "timestamp": str(datetime.now()),
            session_inst.user1.username: False,
            session_inst.user2.username: False
        }
        ChatMessage.objects.create(id=msg_id, chat_session=session_inst, user=self.user, message_detail=message_json)
        return session_inst.user2.id if self.user == session_inst.user1 else session_inst.user1.id

    @database_sync_to_async
    def msg_read(self, msg_id):
        return ChatMessage.meassage_read_true(msg_id)

    @database_sync_to_async
    def read_all_msg(self, room_id, user):
        return ChatMessage.all_msg_read(room_id, user)
