# engagement/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from engagement.views import ProfileViewSet,AlertViewSet,TopFollowerInsightsView

router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'alerts', AlertViewSet, basename='alert')

urlpatterns = [
    path('api/insights/top-follower-changes/', TopFollowerInsightsView.as_view(), name='top-follower-insights'),
]
urlpatterns+=router.urls