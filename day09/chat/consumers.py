from channels.generic.websocket import WebsocketConsumer
import json
from django.contrib.auth.models import User
from django.conf import settings
from . import models

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.chat = models.ChatsName.objects.get(id = self.scope['url_route']['kwargs']['chat_id'])
            self.user = User.objects.get(id = self.scope['url_route']['kwargs']['user_id'])
            self.id_conn = len(settings.ALL_WEB_CONN)
            for conn in settings.ALL_WEB_CONN:
                if conn.chat.id == self.chat.id:
                    conn.send(text_data=json.dumps({
                        'name': self.user.username,
                        'type': '2'
                    }))
            settings.ALL_WEB_CONN.append(self)
            self.accept()
            for mess in list(models.ChatsMessages.objects.filter(chat = self.chat).order_by('created'))[-3:]:
                self.send(text_data=json.dumps({
                    'message': mess.message,
                    'name': mess.user.username,
                    'date': str(mess.created),
                    'type': '1'
                }))
        except:            
            pass

    def disconnect(self, close_code):        
        settings.ALL_WEB_CONN.pop(self.id_conn)
        for conn in settings.ALL_WEB_CONN:
            if conn.chat.id == self.chat.id:
                conn.send(text_data=json.dumps({
                    'name': self.user.username,
                    'type': '3'
                }))
        # Leave room group
#        await self.channel_layer.group_discard(
#            self.room_group_name,
#            self.channel_name
#        )

    # Receive message from WebSocket
    def receive(self, text_data):
        mess = models.ChatsMessages.objects.create(
           user = self.user,
           chat = self.chat,
           message = text_data)
        mess.save()

        for conn in settings.ALL_WEB_CONN:
            if conn.chat.id == self.chat.id:
                conn.send(text_data=json.dumps({
                    'message': mess.message,
                    'name': mess.user.username,
                    'date': str(mess.created),
                    'type': '1'
                }))
