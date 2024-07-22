from django.urls import path
from .views import register, login_view, incoming_messages, sent_messages, send_message, home, delete_message, logout_view

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('messages/', incoming_messages, name='incoming_messages'),  # /messages/ URL'si için
    path('sent/', sent_messages, name='sent_messages'),
    path('send/', send_message, name='send_message'),
    path('delete/<int:message_id>/', delete_message, name='delete_message'),
    path('logout/', logout_view, name='logout'),
]
