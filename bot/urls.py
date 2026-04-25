from django.urls import path

from bot import views

urlpatterns = [
    path("chat/", views.chat_api, name="bot_chat_api"),
    path("chat/opening/", views.chat_opening_prompt, name="bot_chat_opening"),
]
