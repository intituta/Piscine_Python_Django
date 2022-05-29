from django.shortcuts import render, reverse, HttpResponse, HttpResponseRedirect
from . import models

def index(request):
    login = 1
    if not request.user.is_authenticated:
        login = 0
    return render(request, 'chat/templates/index.html', {'chats':models.ChatsName.objects.all(), 'login':login})

def main_chat(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if request.GET.get('id') is not None:
                if models.ChatsName.objects.filter(id = request.GET['id']).exists():
                    chat = models.ChatsName.objects.get(id = request.GET['id'])
                    return render(request, 'chat/templates/main_chat.html', {'chat':chat, 'user':request.user})
    return HttpResponseRedirect(reverse('index'))

def init(request):
    try:
        models.ChatsName.objects.all().delete()
        chat = models.ChatsName.objects.create(name = 'Chat ONE')
        chat.save()
        chat = models.ChatsName.objects.create(name = 'Chat TWO')
        chat.save()
        chat = models.ChatsName.objects.create(name = 'Chat THREE')
        chat.save()        
        
        return HttpResponse("Init data is OK")
    except Exception as e:
        return HttpResponse("Error init data: " + e)
