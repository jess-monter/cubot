from django.urls import path

from apps.chat import views


urlpatterns = [
    path("chat/", views.ConversationView.as_view(), name="conversation-list"),
]
