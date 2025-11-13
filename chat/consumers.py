import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatGroup,Message
from django_jalali.templatetags import jformat
from chat.templatetags.tags import to_persian_numbers

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.group_id = self.scope["url_route"]["kwargs"]["group_id"]
        user = self.scope["user"]
        if await self.check_user(self.group_id,user) :
            await self.channel_layer.group_add(
                self.group_id,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close(403)

    @database_sync_to_async
    def check_user(self, group_id,user):
        group = ChatGroup.objects.get(id=group_id)
        if group.members.filter(user=user).exists():
            return True
        else:
            return False

    @database_sync_to_async
    def save_message(self,text,user,chat_id):
        message = Message.objects.create(user=user,text=text,chat_id=chat_id)
        date = to_persian_numbers(jformat.jformat(message.create,"%H:%M"))
        name = message.user.get_full_name()
        return {
            "date":date,
            "name":name,
            "user_id" :user.id,
        }


    async def disconnect(self, code):
        print(code)

    async def receive(self, text_data=None, bytes_data=None):
        if text_data :
            data = json.loads(text_data)
            message = data["message"]
            other_data = await self.save_message(message,self.scope["user"],self.group_id)
            await self.channel_layer.group_send(
                self.group_id,
                {
                    "type":"send_message",
                    "data" : json.dumps({
                        "message": message,
                        "date": other_data["date"],
                        "name": other_data["name"],
                        "user_id": other_data["user_id"]
                    }),
                }
            )

    async def send_message(self,event):
        await self.send(event["data"])