from django.urls import path

from .views import RegisterView, UserActivityView


urlpatterns = [
    path('', RegisterView.as_view(), name='register'),
    path('activity', UserActivityView.as_view(), name='activity')
]
