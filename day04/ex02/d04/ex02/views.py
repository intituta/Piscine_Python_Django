import datetime
from django.shortcuts import render
from django.conf import settings
from .forms import PostForm


def get_name(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            with open(settings.LOG_URL, "a") as file:
                file.write(f"{str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))} ")
                file.write(text)
                file.write("\n")
            with open(settings.LOG_URL, "r") as log:
                history = log.readlines()
            return render(request, 'ex02/index.html', context={'text': history, 'form': form})
    else:
        with open(settings.LOG_URL, "a") as o:
            pass
        with open(settings.LOG_URL, "r") as log:
            history = log.readlines()
        form = PostForm()
    return render(request, 'ex02/index.html', context={'text': history, 'form': form})
