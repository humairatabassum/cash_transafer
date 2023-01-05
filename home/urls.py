from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name="home"),
    path('validation', views.validation, name="validation"),
    path('signin', views.signin, name="signin"),
    path('register', views.register, name="register"),
    path('logout', views.logout, name='logout'),
    path('sharedMoney', views.sharedMoney, name='sharedMoney'),
    path('chat_box', views.chat_box, name='chat_box'),
    path('show_message', views.show_message, name='show_message'),
]
