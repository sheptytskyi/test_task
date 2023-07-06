from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, PostAnalyticsView

router = DefaultRouter()
router.register('', viewset=PostViewSet, basename='post')


urlpatterns = [
    path('', include(router.urls)),
    path('analytics', PostAnalyticsView.as_view(), name='analytics'),
]
