from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('init/', views.init, name='init'),
    path('main/', views.main_chat, name='main'),
#    path('list/', ChatList.as_view(), name='list'),
#    path('login/', LoginPage.as_view(), name='login'),
#    path('', views.index, name='index'),
#    path('<str:room_name>/', views.room, name='room-detail'),
#    path('logout/', Logout.as_view(), name='logout'),
]