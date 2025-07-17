from django.urls import path

from accounts.views import UpdateTelegramInfoView

urlpatterns = [
    path('me/telegram/', UpdateTelegramInfoView.as_view(), name='telegram-update')
]

