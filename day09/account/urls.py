from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.index, name='index'),
    path('get_content/', views.GetContent.as_view(), name='content'),
    path('logout/', views.disconnect, name='logout'),
]